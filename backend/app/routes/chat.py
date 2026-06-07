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

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return jsonify({
            "status": "error",
            "reason": "GOOGLE_API_KEY environment variable is not set.",
        }), 500

    model = "gemini-1.5-flash-latest"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}?key={api_key}"
        r = req.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return jsonify({
                "status": "ok",
                "model": data.get("name"),
                "output_token_limit": data.get("outputTokenLimit"),
                "key_prefix": api_key[:8] + "...",
            }), 200
        else:
            err = r.json().get("error", {})
            return jsonify({
                "status": "error",
                "http_status": r.status_code,
                "reason": err.get("message", r.text),
                "key_prefix": api_key[:8] + "...",
            }), 200
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 500

