from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.engine import hybrid_controller

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("", methods=["POST"])
@jwt_required()
def chat():
    """
    POST /api/v1/chat
    Send a user query to the hybrid AI controller.
    Body: { query, current_topic_id }
    """
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    topic_id = data.get("current_topic_id", None)

    if not query:
        return jsonify({"error": "A 'query' field is required."}), 400

    user_id = get_jwt_identity()

    # Pass the request to the Hybrid Controller
    result = hybrid_controller.process(
        query=query,
        user_id=user_id,
        topic_id=topic_id,
    )

    # Return the structured response
    return jsonify({
        "response": result["response"],
        "source": result["source"],
        "intent": result["intent"],
        "topic_context": result["topic_context"],
    }), 200


@chat_bp.route("/health", methods=["GET"])
def gemini_health():
    """
    GET /api/v1/chat/health
    Public endpoint — checks if the Gemini API key is configured and reachable.
    Use this to diagnose AI Mentor connection issues without needing to log in.
    """
    import os
    import requests as req
    from app.engine.nlp_module import get_gemini_api_key

    api_key = get_gemini_api_key()

    # Scan env for keys containing helpful keywords to aid diagnostic
    env_keys = []
    for k, v in os.environ.items():
        k_upper = k.upper()
        if any(x in k_upper for x in ["API", "KEY", "GOOGLE", "GEMINI"]):
            val_str = v.strip()
            # Mask value but show first few characters (e.g. AIzaSy or AQ.) for verification
            masked = val_str[:8] + "..." if len(val_str) > 8 else "..."
            env_keys.append({"key": k, "preview": masked, "length": len(val_str)})

    if not api_key:
        return jsonify({
            "status": "error",
            "reason": "Gemini API key not found. Checked GOOGLE_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, and scanned env for AIza/AQ prefix fallbacks.",
            "available_env_keys": env_keys,
        }), 500

    model = "gemini-1.5-flash-latest"
    list_all = request.args.get("list_models", "").lower() == "true"
    try:
        if list_all:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        else:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}?key={api_key}"
        
        r = req.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if list_all:
                model_names = [m.get("name") for m in data.get("models", [])]
                return jsonify({
                    "status": "ok",
                    "models": model_names,
                    "key_preview": api_key[:8] + "...",
                    "available_env_keys": env_keys,
                }), 200
            else:
                return jsonify({
                    "status": "ok",
                    "model": data.get("name"),
                    "output_token_limit": data.get("outputTokenLimit"),
                    "key_preview": api_key[:8] + "...",
                    "available_env_keys": env_keys,
                }), 200
        else:
            err = r.json().get("error", {})
            return jsonify({
                "status": "error",
                "http_status": r.status_code,
                "reason": err.get("message", r.text),
                "key_preview": api_key[:8] + "...",
                "available_env_keys": env_keys,
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "reason": str(e),
            "available_env_keys": env_keys,
        }), 500

