from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Lesson, UserProgress

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("", methods=["GET"])
@progress_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_full_progress():
    """
    GET /api/v1/progress
    GET /api/v1/progress/summary
    Return the full progress summary for the authenticated user.
    Includes per-topic status and overall completion %.
    """
    user_id = get_jwt_identity()
    lessons = Lesson.query.order_by(Lesson.order_index).all()

    progress_map = {
        p.topic_id: p
        for p in UserProgress.query.filter_by(user_id=user_id).all()
    }

    topic_breakdown = []
    mastered_count = 0
    last_topic = None
    last_accessed_dt = None

    for lesson in lessons:
        p = progress_map.get(lesson.id)
        status = p.status if p else "not_started"
        score = p.practice_score if p else None
        is_mastered = status == "mastered"

        if is_mastered:
            mastered_count += 1

        # Track most recently accessed topic
        if p and p.last_accessed:
            if last_accessed_dt is None or p.last_accessed > last_accessed_dt:
                last_accessed_dt = p.last_accessed
                last_topic = {"id": lesson.id, "title": lesson.title, "status": status}

        topic_breakdown.append({
            "id": lesson.id,
            "topic_id": lesson.id,
            "title": lesson.title,
            "status": status,
            "is_mastered": is_mastered,
            "practice_score": score,
            "mastery_score": score,
            "order_index": lesson.order_index,
        })

    total_topics = len(lessons)
    overall_pct = round((mastered_count / total_topics) * 100) if total_topics else 0

    return jsonify({
        "overall_percentage": overall_pct,
        "overall_progress_percentage": overall_pct,
        "mastered_count": mastered_count,
        "total_topics": total_topics,
        "all_complete": mastered_count == total_topics and total_topics > 0,
        "last_accessed_topic": last_topic,
        "topics": topic_breakdown,
    }), 200


@progress_bp.route("/<string:topic_id>", methods=["GET"])
@jwt_required()
def get_topic_progress(topic_id):
    """
    GET /api/v1/progress/<topic_id>
    Return detailed progress for one specific topic.
    """
    user_id = get_jwt_identity()
    lesson = db.session.get(Lesson, topic_id)
    if not lesson:
        return jsonify({"error": "Topic not found."}), 404

    progress = UserProgress.query.filter_by(
        user_id=user_id, topic_id=topic_id
    ).first()

    return jsonify({
        "topic_id": topic_id,
        "topic_title": lesson.title,
        "status": progress.status if progress else "not_started",
        "practice_score": progress.practice_score if progress else None,
        "attempt_count": progress.attempt_count if progress else 0,
        "last_accessed": (
            progress.last_accessed.isoformat() if progress and progress.last_accessed else None
        ),
    }), 200
