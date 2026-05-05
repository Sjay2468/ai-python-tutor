from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models import Lesson, UserProgress

lessons_bp = Blueprint("lessons", __name__)


def _get_or_create_progress(user_id, topic_id):
    """Fetch or create a UserProgress record for a user+topic pair."""
    progress = UserProgress.query.filter_by(
        user_id=user_id, topic_id=topic_id
    ).first()
    if not progress:
        progress = UserProgress(
            user_id=user_id, topic_id=topic_id, status="not_started"
        )
        db.session.add(progress)
        db.session.commit()
    return progress


@lessons_bp.route("", methods=["GET"])
@jwt_required()
def get_all_lessons():
    """
    GET /api/v1/lessons
    Return list of all 9 topics with the user's current study status.
    """
    user_id = get_jwt_identity()
    lessons = Lesson.query.order_by(Lesson.order_index).all()

    # Build a map of topic_id → progress for this user
    progress_map = {
        p.topic_id: p
        for p in UserProgress.query.filter_by(user_id=user_id).all()
    }

    result = []
    for lesson in lessons:
        p = progress_map.get(lesson.id)
        status = p.status if p else "not_started"
        score = p.practice_score if p else None
        result.append(lesson.to_dict(status=status))

    return jsonify({"lessons": result}), 200


@lessons_bp.route("/<string:topic_id>", methods=["GET"])
@jwt_required()
def get_lesson(topic_id):
    """
    GET /api/v1/lessons/<topic_id>
    Return the full lesson content for a specific topic.
    """
    user_id = get_jwt_identity()
    lesson = db.session.get(Lesson, topic_id)
    if not lesson:
        return jsonify({"error": "Lesson not found."}), 404

    progress = _get_or_create_progress(user_id, topic_id)

    # Update last_accessed timestamp
    progress.last_accessed = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({
        "lesson": lesson.to_full_dict(
            status=progress.status,
            score=progress.practice_score
        )
    }), 200


@lessons_bp.route("/<string:topic_id>/study", methods=["POST"])
@jwt_required()
def mark_studied(topic_id):
    """
    POST /api/v1/lessons/<topic_id>/study
    Mark a topic as 'studied'. Enables the Practice feature for that topic.
    Only upgrades status — does not downgrade from 'mastered'.
    """
    user_id = get_jwt_identity()
    lesson = db.session.get(Lesson, topic_id)
    if not lesson:
        return jsonify({"error": "Lesson not found."}), 404

    progress = _get_or_create_progress(user_id, topic_id)

    # Don't downgrade if already mastered
    if progress.status == "not_started":
        progress.status = "studied"
        progress.last_accessed = datetime.now(timezone.utc)
        db.session.commit()

    return jsonify({
        "message": f"'{lesson.title}' marked as studied.",
        "topic_id": topic_id,
        "status": progress.status,
    }), 200
