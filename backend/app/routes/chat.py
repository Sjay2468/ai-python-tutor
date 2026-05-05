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
