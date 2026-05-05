"""
Rule-Based Engine
-----------------
Loads all JSON rule files from knowledge_base/, matches user queries
against keyword lists, classifies intent, and returns a grounding snippet
when confidence >= 0.7.

Logic (from PRD §11.2):
  1. Tokenise and lowercase the query.
  2. For each rule entry, compute: matched_keywords / total_keywords_in_rule.
  3. Select the rule with the highest confidence score.
  4. If score >= 0.7 → return that rule's response as grounding context.
  5. If score < 0.7  → no grounding; classify as concept_question.
  6. If no keyword matches at all → out_of_scope.
"""

import os
import json
import re
from dataclasses import dataclass, field
from typing import Optional

# Resolve the knowledge_base directory relative to this file
_KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")

# Intent constants (match PRD FR-RB-02)
INTENT_CONCEPT = "concept_question"
INTENT_HINT = "hint_request"
INTENT_ERROR = "error_explanation"
INTENT_OOS = "out_of_scope"

CONFIDENCE_THRESHOLD = 0.7


@dataclass
class RuleMatch:
    """Holds the result of a rule-base lookup."""
    intent: str
    confidence: float
    rule_id: Optional[str] = None
    grounding_snippet: Optional[str] = None   # Pre-authored response used as GPT-4 context
    topic_id: Optional[str] = None
    is_out_of_scope: bool = False


class RuleBasedEngine:
    """Singleton-safe rule engine. Call load() once at app startup."""

    def __init__(self):
        self._rules: list[dict] = []   # Flat list of all rule entries across all files
        self._loaded = False

    def load(self) -> None:
        """Load all JSON rule files from knowledge_base/."""
        self._rules = []
        kb_dir = os.path.abspath(_KB_DIR)
        if not os.path.isdir(kb_dir):
            print(f"[WARNING] knowledge_base/ not found at {kb_dir}")
            return

        for filename in os.listdir(kb_dir):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(kb_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                topic_id = data.get("lesson_id") or data.get("lesson_ids", [None])[0]
                for rule in data.get("rules", []):
                    rule["_topic_id"] = topic_id
                    self._rules.append(rule)
            except (json.JSONDecodeError, OSError) as e:
                print(f"[WARNING] Failed to load {filename}: {e}")

        self._loaded = True
        print(f"[OK] Rule engine loaded {len(self._rules)} rules from {kb_dir}")

    def _tokenize(self, text: str) -> list[str]:
        """Lowercase and split text into word tokens, stripping punctuation."""
        text = text.lower()
        tokens = re.findall(r"[a-z0-9_%]+", text)
        return tokens

    def match(self, query: str, topic_id: Optional[str] = None) -> RuleMatch:
        """
        Match a user query against all loaded rules.
        Returns a RuleMatch with the best result.
        """
        if not self._loaded:
            self.load()

        query_tokens = set(self._tokenize(query))
        if not query_tokens:
            return RuleMatch(intent=INTENT_OOS, confidence=0.0, is_out_of_scope=True)

        best_score = 0.0
        best_rule = None

        for rule in self._rules:
            keywords = [k.lower() for k in rule.get("keywords", [])]
            if not keywords:
                continue

            # Confidence = proportion of the rule's keywords found in the query
            matched = sum(1 for kw in keywords if kw in query_tokens or kw in query.lower())
            score = matched / len(keywords)

            if score > best_score:
                best_score = score
                best_rule = rule

        # --- Decision logic (PRD §11.2) ---
        if best_score == 0.0:
            # No keyword overlap at all → out of scope
            return RuleMatch(intent=INTENT_OOS, confidence=0.0, is_out_of_scope=True)

        intent = best_rule.get("intent", INTENT_CONCEPT)

        # Immediately handle out-of-scope rules
        if intent == INTENT_OOS:
            return RuleMatch(
                intent=INTENT_OOS,
                confidence=best_score,
                rule_id=best_rule.get("id"),
                grounding_snippet=best_rule.get("response"),
                is_out_of_scope=True,
            )

        if best_score >= CONFIDENCE_THRESHOLD:
            # High confidence → use rule response as grounding snippet
            return RuleMatch(
                intent=intent,
                confidence=best_score,
                rule_id=best_rule.get("id"),
                grounding_snippet=best_rule.get("response"),
                topic_id=best_rule.get("_topic_id") or topic_id,
            )
        else:
            # Low confidence → no grounding; classify as concept_question
            return RuleMatch(
                intent=INTENT_CONCEPT,
                confidence=best_score,
                topic_id=topic_id,
            )


# Module-level singleton — imported by hybrid_controller.py
rule_engine = RuleBasedEngine()
