from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    """
    POST /api/v1/chat
    Send a user query to the hybrid AI controller.
    Body: { query, current_topic_id }

    NOTE: Full hybrid AI implementation done in Phase 4.
    This stub validates the request and returns a placeholder response.
    """
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    topic_id = data.get("current_topic_id", None)

    if not query:
        return jsonify({"error": "A 'query' field is required."}), 400

    # Phase 4 will replace this with the real hybrid controller call
    return jsonify({
        "response": "The AI tutor is being set up. Full responses will be available in Phase 4.",
        "source": "placeholder",
        "topic_context": topic_id,
    }), 200
