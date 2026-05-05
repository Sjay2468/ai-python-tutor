"""
NLP Module — GPT-4 Integration
--------------------------------
Builds structured prompts from PRD §10 templates and calls the OpenAI API.
Handles timeouts, API errors, and rate limiting with graceful fallback signals.

Rate limiting: 20 calls / user / hour (tracked in memory; use Redis in prod).
Timeout: 8 seconds client-side (PRD NFR-PF-04).
"""

import os
import time
import hashlib
from collections import defaultdict
from typing import Optional

from openai import OpenAI, APITimeoutError, APIError, RateLimitError

# ── Rate-limit tracking (in-memory; sufficient for prototype) ──
# Structure: { user_hash: [(timestamp, ...), ...] }
_CALL_LOG: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT = 20          # calls per user per hour
_RATE_WINDOW = 3600       # seconds (1 hour)

# ── GPT-4 parameters (PRD §10.1) ──
_MODEL = "gpt-4"
_MAX_TOKENS = 300
_TEMPERATURE = 0.3
_TIMEOUT = 8.0            # seconds

# ── Prompt templates (PRD §10.2 / §10.3) ──
_SYSTEM_PROMPT = """You are a friendly Python tutor helping absolute beginners.
You ONLY explain beginner Python concepts: variables, data types, operators, \
conditionals, loops, functions, lists, dictionaries, basic errors, and input/output.
Do NOT explain advanced topics (OOP, file handling, external libraries, etc.).
Keep all explanations under 150 words.
Use simple English. Avoid technical jargon.
Use a real-world analogy if helpful.
If the question is unrelated to beginner Python, respond only with:
"I can only help with beginner Python topics."
Current lesson context: {topic_title}"""

_USER_PROMPT = """Rule-base grounding (if available): {rule_snippet}

Student question: {user_query}

Please explain this to a complete beginner."""


def _hash_user_id(user_id: str) -> str:
    """SHA-256 hash of user ID for privacy-safe rate-limit tracking."""
    return hashlib.sha256(user_id.encode()).hexdigest()


def _is_rate_limited(user_id: str) -> bool:
    """Return True if this user has exceeded 20 GPT-4 calls in the last hour."""
    uid_hash = _hash_user_id(user_id)
    now = time.time()
    # Remove calls older than the rate window
    _CALL_LOG[uid_hash] = [t for t in _CALL_LOG[uid_hash] if now - t < _RATE_WINDOW]
    return len(_CALL_LOG[uid_hash]) >= _RATE_LIMIT


def _log_call(user_id: str) -> None:
    """Record a new GPT-4 call timestamp for rate limiting."""
    _CALL_LOG[_hash_user_id(user_id)].append(time.time())


class NLPResult:
    """Holds the outcome of a GPT-4 API call."""
    def __init__(
        self,
        text: str,
        source: str,  # "nlp_grounded" | "nlp_only" | "fallback" | "rate_limited"
        latency_ms: int = 0,
        error: Optional[str] = None,
    ):
        self.text = text
        self.source = source
        self.latency_ms = latency_ms
        self.error = error


def call_gpt4(
    user_query: str,
    topic_title: str,
    user_id: str,
    rule_snippet: Optional[str] = None,
) -> NLPResult:
    """
    Call the GPT-4 API with a structured prompt.

    Returns NLPResult. If the API fails or times out, returns a fallback signal
    so the Hybrid Controller can substitute the rule-based response.

    Args:
        user_query:   The student's question.
        topic_title:  The lesson topic currently being studied.
        user_id:      The authenticated user's ID (for rate limiting).
        rule_snippet: Pre-authored rule response used as grounding context (optional).
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return NLPResult(
            text="",
            source="fallback",
            error="OPENAI_API_KEY not configured.",
        )

    # Rate limiting check (FR-NLP-05)
    if _is_rate_limited(user_id):
        return NLPResult(
            text="",
            source="rate_limited",
            error="Rate limit reached (20 calls/hour). Rule-based response used.",
        )

    # Build prompts
    system_msg = _SYSTEM_PROMPT.format(topic_title=topic_title or "General Python")
    user_msg = _USER_PROMPT.format(
        rule_snippet=rule_snippet or "None available.",
        user_query=user_query,
    )
    source = "nlp_grounded" if rule_snippet else "nlp_only"

    client = OpenAI(api_key=api_key, timeout=_TIMEOUT)
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_msg},
            ],
            max_tokens=_MAX_TOKENS,
            temperature=_TEMPERATURE,
        )
        latency_ms = int((time.time() - start) * 1000)
        _log_call(user_id)

        text = response.choices[0].message.content.strip()
        return NLPResult(text=text, source=source, latency_ms=latency_ms)

    except APITimeoutError:
        latency_ms = int((time.time() - start) * 1000)
        return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                         error="GPT-4 timeout (>8s).")
    except RateLimitError:
        return NLPResult(text="", source="fallback",
                         error="OpenAI rate limit exceeded.")
    except APIError as e:
        return NLPResult(text="", source="fallback",
                         error=f"OpenAI API error: {e.status_code}")
    except Exception as e:
        return NLPResult(text="", source="fallback",
                         error=f"Unexpected error: {str(e)}")
