"""
NLP Module — Google Gemini REST API Integration
-------------------------------------------------
Calls the Gemini API directly via HTTP using the 'requests' library.

Dynamic token limits:
  - At startup the module queries the Gemini model metadata endpoint to
    discover the model's true outputTokenLimit and uses that as the cap.
  - Falls back to 8192 if the metadata call fails (safe large default).
  - No hard-coded word limits anywhere — the model decides how long the
    response should be to fully answer the question.

Rate limiting: 20 calls / user / hour (in-memory; use Redis in prod).
"""

import os
import time
import hashlib
import requests
from collections import defaultdict
from typing import Optional

# ── Rate-limit tracking (in-memory) ──────────────────────────────────────────
_CALL_LOG: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT = 20        # calls per user per hour
_RATE_WINDOW = 3600     # seconds (1 hour)

# ── Gemini REST API config ────────────────────────────────────────────────────
_MODEL    = "gemini-flash-latest"
_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
_TIMEOUT  = 30.0   # generous timeout — never cut off a long response mid-flight

# ── Dynamic token limit ───────────────────────────────────────────────────────
_FALLBACK_MAX_TOKENS = 8192   # used if metadata fetch fails


def _fetch_model_output_limit(api_key: str) -> int:
    """
    Query the Gemini model metadata to get its real outputTokenLimit.
    Returns the limit, or _FALLBACK_MAX_TOKENS on any error.
    This is called once lazily and cached in _MODEL_MAX_TOKENS.
    """
    try:
        url = f"{_API_BASE}/{_MODEL}?key={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            limit = resp.json().get("outputTokenLimit", _FALLBACK_MAX_TOKENS)
            return int(limit)
    except Exception:
        pass
    return _FALLBACK_MAX_TOKENS


# Module-level cache: populated on first call, then reused for all subsequent calls
_MODEL_MAX_TOKENS: Optional[int] = None


def _get_max_tokens(api_key: str) -> int:
    """Return the cached dynamic token limit, fetching it once if needed."""
    global _MODEL_MAX_TOKENS
    if _MODEL_MAX_TOKENS is None:
        _MODEL_MAX_TOKENS = _fetch_model_output_limit(api_key)
        print(f"[Gemini] Dynamic outputTokenLimit for '{_MODEL}': {_MODEL_MAX_TOKENS}")
    return _MODEL_MAX_TOKENS


# ── Prompt templates ──────────────────────────────────────────────────────────
# No word-count instruction — let the model produce a complete, natural answer.
_SYSTEM_PROMPT = (
    "You are a friendly and thorough Python tutor helping absolute beginners. "
    "You ONLY explain beginner Python concepts: variables, data types, operators, "
    "conditionals, loops, functions, lists, dictionaries, basic errors, and input/output. "
    "Do NOT explain advanced topics (OOP, file handling, external libraries, etc.). "
    "Always give a COMPLETE answer — never stop mid-sentence or mid-explanation. "
    "Use clear, simple English with real-world analogies where helpful. "
    "Include a short code example when it would help illustrate the concept. "
    "If the question is unrelated to beginner Python, respond only with: "
    "\"I can only help with beginner Python topics.\"\n"
    "Current lesson context: {topic_title}"
)

_USER_PROMPT = (
    "Grounding context (rule-based, if available): {rule_snippet}\n\n"
    "Student question: {user_query}\n\n"
    "Please give a full, complete explanation. Do not truncate your response."
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()


def _is_rate_limited(user_id: str) -> bool:
    uid_hash = _hash_user_id(user_id)
    now = time.time()
    _CALL_LOG[uid_hash] = [t for t in _CALL_LOG[uid_hash] if now - t < _RATE_WINDOW]
    return len(_CALL_LOG[uid_hash]) >= _RATE_LIMIT


def _log_call(user_id: str) -> None:
    _CALL_LOG[_hash_user_id(user_id)].append(time.time())


def _is_response_complete(data: dict) -> bool:
    """
    Check the Gemini finishReason field.
    'STOP' means the model finished naturally.
    'MAX_TOKENS' means it was cut off — we log a warning but still return the text
    rather than dropping the response entirely.
    """
    try:
        reason = data["candidates"][0].get("finishReason", "STOP")
        if reason == "MAX_TOKENS":
            print(f"[WARNING] Gemini hit MAX_TOKENS for model '{_MODEL}'. "
                  f"Consider raising outputTokenLimit or splitting the prompt.")
        return True   # return text regardless — partial is better than nothing
    except (KeyError, IndexError):
        return True


# ── Result class ──────────────────────────────────────────────────────────────

class NLPResult:
    """Holds the outcome of a Gemini API call."""
    def __init__(
        self,
        text: str,
        source: str,   # "nlp_grounded" | "nlp_only" | "fallback" | "rate_limited"
        latency_ms: int = 0,
        error: Optional[str] = None,
        finish_reason: str = "STOP",
    ):
        self.text         = text
        self.source       = source
        self.latency_ms   = latency_ms
        self.error        = error
        self.finish_reason = finish_reason


# ── Main API call ─────────────────────────────────────────────────────────────

def call_gemini(
    user_query: str,
    topic_title: str,
    user_id: str,
    rule_snippet: Optional[str] = None,
) -> NLPResult:
    """
    Call the Google Gemini REST API with a fully dynamic token limit.

    - Token limit is fetched from the model metadata on first call (cached).
    - No word-count cap anywhere in the pipeline.
    - Timeout is 30s to allow longer responses to complete without being cut off.
    - If the model hits MAX_TOKENS, we still return the partial text with a warning
      rather than discarding the response.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return NLPResult(text="", source="fallback",
                         error="GOOGLE_API_KEY not configured.")

    if _is_rate_limited(user_id):
        return NLPResult(text="", source="rate_limited",
                         error="Rate limit reached (20 calls/hour).")

    # Build prompts
    system_msg  = _SYSTEM_PROMPT.format(topic_title=topic_title or "General Python")
    user_msg    = _USER_PROMPT.format(
        rule_snippet=rule_snippet or "None available.",
        user_query=user_query,
    )
    full_prompt = f"{system_msg}\n\n{user_msg}"
    source      = "nlp_grounded" if rule_snippet else "nlp_only"

    # Dynamically determine the max tokens this model supports
    max_tokens = _get_max_tokens(api_key)

    url = f"{_API_BASE}/{_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": max_tokens,  # use the model's full capacity
            "temperature":     0.4,         # slightly higher for more natural prose
            "candidateCount":  1,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    }

    start = time.time()
    try:
        resp       = requests.post(url, json=payload, timeout=_TIMEOUT)
        latency_ms = int((time.time() - start) * 1000)

        if resp.status_code != 200:
            err_body = resp.json() if resp.content else {}
            err_msg  = err_body.get("error", {}).get("message", resp.text)
            return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                             error=f"Gemini API error {resp.status_code}: {err_msg}")

        data = resp.json()

        # Check finish reason (logs warning on MAX_TOKENS but doesn't discard)
        _is_response_complete(data)
        finish_reason = (
            data.get("candidates", [{}])[0].get("finishReason", "STOP")
        )

        # Concatenate all parts (Gemini may split long responses across parts)
        candidates = data.get("candidates", [])
        if not candidates:
            return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                             error="Gemini returned no candidates.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text  = "".join(p.get("text", "") for p in parts).strip()

        if not text:
            return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                             error="Gemini returned an empty response.")

        _log_call(user_id)
        return NLPResult(
            text=text,
            source=source,
            latency_ms=latency_ms,
            finish_reason=finish_reason,
        )

    except requests.Timeout:
        latency_ms = int((time.time() - start) * 1000)
        return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                         error=f"Gemini request timed out after {_TIMEOUT}s.")
    except requests.RequestException as e:
        latency_ms = int((time.time() - start) * 1000)
        return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                         error=f"Network error: {str(e)}")
    except Exception as e:
        latency_ms = int((time.time() - start) * 1000)
        return NLPResult(text="", source="fallback", latency_ms=latency_ms,
                         error=f"Unexpected error: {str(e)}")
