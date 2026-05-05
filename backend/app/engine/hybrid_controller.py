"""
Hybrid Controller
------------------
The single orchestrator between the Rule-Based Engine and the GPT-4 NLP module.
No response is returned to the client without passing through here (PRD FR-HC-01).

Decision flow (PRD §12.1):
  Step 1 → Intent Classification  (rule engine)
  Step 2 → Rule KB Lookup         (rule engine)
  Step 3 → GPT-4 API Call         (nlp_module)
  Step 4 → Validation             (off-topic / length / coherence checks)
  → Return tagged response to client
"""

import hashlib
import time
from typing import Optional
from datetime import datetime, timezone

from .rule_engine import rule_engine, INTENT_OOS
from .nlp_module import call_gpt4

# Validation constants (PRD §12.2)
_MAX_RESPONSE_WORDS = 300
_OOS_MARKER = "I can only help with beginner Python topics"

# Terms that flag an advanced/off-topic GPT-4 response
_BANNED_ADVANCED_TERMS = [
    "class ", "inheritance", "polymorphism", "encapsulation",
    "open()", "with open", "file handling", "pandas", "numpy",
    "matplotlib", "django", "flask route",   # Flask itself is backend; not taught
    "decorators", "__init__", "self.", "object-oriented",
]


def _validate_response(text: str, query: str) -> bool:
    """
    Returns True if the GPT-4 response passes all validation checks.
    Checks (PRD §12.2):
      1. Off-topic check   — response contains OOS marker
      2. Length check      — response > 300 words
      3. Advanced content  — response mentions banned advanced terms
    """
    if not text:
        return False

    # Check 1: GPT-4 itself flagged the query as out-of-scope
    if _OOS_MARKER.lower() in text.lower():
        return False

    # Check 2: Response too long
    if len(text.split()) > _MAX_RESPONSE_WORDS:
        return False

    # Check 3: Advanced / off-topic content
    text_lower = text.lower()
    for term in _BANNED_ADVANCED_TERMS:
        if term.lower() in text_lower:
            return False

    return True


def _get_topic_title(topic_id: Optional[str]) -> str:
    """Safely retrieve a lesson title from the DB without circular imports."""
    if not topic_id:
        return "General Python Basics"
    try:
        from app.models import Lesson
        from flask import current_app
        with current_app.app_context():
            lesson = Lesson.query.get(topic_id)
            return lesson.title if lesson else "General Python Basics"
    except Exception:
        return "General Python Basics"


def _log_chat(user_id: str, topic_id: Optional[str], intent: str,
              source: str, latency_ms: int) -> None:
    """Write a privacy-safe analytics entry to ChatLog (no query text stored)."""
    try:
        from app import db
        from app.models import ChatLog
        uid_hash = hashlib.sha256(user_id.encode()).hexdigest()
        log = ChatLog(
            user_id_hash=uid_hash,
            topic_context=topic_id,
            intent_category=intent if intent in (
                "concept_question", "hint_request",
                "error_explanation", "out_of_scope"
            ) else "concept_question",
            response_source=source if source in (
                "rule_based", "nlp_grounded", "nlp_only", "fallback"
            ) else "fallback",
            latency_ms=latency_ms,
            timestamp=datetime.now(timezone.utc),
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        # Logging failure must never break the response pipeline
        print(f"[WARNING] ChatLog write failed: {e}")


class HybridController:
    """
    Orchestrates the full tutoring pipeline for a single user query.
    Instantiate once; call process() per request.
    """

    def process(
        self,
        query: str,
        user_id: str,
        topic_id: Optional[str] = None,
    ) -> dict:
        """
        Run the 4-step hybrid pipeline and return a response dict.

        Returns:
            {
                "response": str,
                "source":   "rule_based" | "nlp_grounded" | "nlp_only" | "fallback",
                "intent":   str,
                "topic_context": str | None,
            }
        """
        pipeline_start = time.time()

        # ── Step 1 & 2: Intent Classification + Rule Lookup ──────────────────
        match = rule_engine.match(query, topic_id=topic_id)

        # Immediately return for out-of-scope queries (FR-HC-02, FR-CH-05)
        if match.is_out_of_scope:
            latency_ms = int((time.time() - pipeline_start) * 1000)
            fallback_text = (
                match.grounding_snippet
                or "I can only help with beginner Python topics. "
                   "Try asking about variables, loops, functions, or errors."
            )
            _log_chat(user_id, topic_id, INTENT_OOS, "rule_based", latency_ms)
            return {
                "response": fallback_text,
                "source": "rule_based",
                "intent": INTENT_OOS,
                "topic_context": topic_id,
            }

        # ── Step 3: GPT-4 Call ───────────────────────────────────────────────
        topic_title = _get_topic_title(topic_id)
        nlp_result = call_gpt4(
            user_query=query,
            topic_title=topic_title,
            user_id=user_id,
            rule_snippet=match.grounding_snippet,   # None if confidence < 0.7
        )

        # ── Step 4: Validation ───────────────────────────────────────────────
        latency_ms = int((time.time() - pipeline_start) * 1000)

        if nlp_result.source in ("fallback", "rate_limited"):
            # API failed or rate-limited → use rule grounding or generic fallback
            final_text = (
                match.grounding_snippet
                or "I'm having trouble connecting right now. "
                   "Here's what I know: please check the lesson content "
                   "for this topic and try again shortly."
            )
            final_source = "rule_based"

        elif _validate_response(nlp_result.text, query):
            final_text = nlp_result.text
            final_source = nlp_result.source   # nlp_grounded or nlp_only
            latency_ms = nlp_result.latency_ms

        else:
            # GPT-4 response failed validation → rule-based fallback (FR-HC-03)
            final_text = (
                match.grounding_snippet
                or "I can only help with beginner Python topics. "
                   "Try asking about variables, loops, or functions."
            )
            final_source = "fallback"

        # ── Log and return ───────────────────────────────────────────────────
        _log_chat(user_id, topic_id, match.intent, final_source, latency_ms)

        return {
            "response": final_text,
            "source": final_source,
            "intent": match.intent,
            "topic_context": topic_id,
        }


# Module-level singleton
hybrid_controller = HybridController()
