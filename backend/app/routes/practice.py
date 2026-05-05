from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models import Lesson, PracticeQuestion, UserProgress

practice_bp = Blueprint("practice", __name__)

# Mastery threshold per PRD (FR-PA-05)
MASTERY_THRESHOLD = 70


def _get_or_create_progress(user_id, topic_id):
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


@practice_bp.route("/<string:topic_id>", methods=["GET"])
@jwt_required()
def get_practice_questions(topic_id):
    """
    GET /api/v1/practice/<topic_id>
    Return all practice questions for a topic (without revealing correct answer).
    Only available if the topic has been studied.
    """
    user_id = get_jwt_identity()
    lesson = db.session.get(Lesson, topic_id)
    if not lesson:
        return jsonify({"error": "Topic not found."}), 404

    progress = _get_or_create_progress(user_id, topic_id)
    if progress.status == "not_started":
        return jsonify({
            "error": "Please read and mark this lesson as studied before attempting practice."
        }), 403

    questions = PracticeQuestion.query.filter_by(topic_id=topic_id).all()
    if not questions:
        return jsonify({"error": "No practice questions found for this topic."}), 404

    return jsonify({
        "topic_id": topic_id,
        "topic_title": lesson.title,
        "question_count": len(questions),
        "questions": [q.to_dict() for q in questions],
    }), 200


@practice_bp.route("/<string:topic_id>/submit", methods=["POST"])
@jwt_required()
def submit_answer(topic_id):
    """
    POST /api/v1/practice/<topic_id>/submit
    Submit an answer for one question. Returns correctness + hint.
    Body: { question_id, selected_option, attempt_number }
    """
    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    selected = data.get("selected_option", "").upper()
    attempt = data.get("attempt_number", 1)

    if not question_id or selected not in ("A", "B", "C", "D"):
        return jsonify({"error": "question_id and selected_option (A/B/C/D) are required."}), 400

    question = db.session.get(PracticeQuestion, question_id)
    if not question or question.topic_id != topic_id:
        return jsonify({"error": "Question not found for this topic."}), 404

    is_correct = selected == question.correct_option

    # Progressive hint selection (FR-PA-03)
    hint = None
    correct_option_revealed = None
    if not is_correct:
        if attempt == 1:
            hint = question.hint_1
        elif attempt == 2:
            hint = question.hint_2
        else:
            # Attempt 3+: reveal reasoning and the correct answer
            hint = question.hint_3
            correct_option_revealed = question.correct_option

    return jsonify({
        "correct": is_correct,
        "hint": hint,
        "correct_option": correct_option_revealed,
    }), 200


@practice_bp.route("/<string:topic_id>/complete", methods=["POST"])
@jwt_required()
def complete_practice(topic_id):
    """
    POST /api/v1/practice/<topic_id>/complete
    Submit final score for a topic session. Updates mastery status.
    Body: { correct_count, total_count }
    """
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    correct = data.get("correct_count")
    total = data.get("total_count")

    if correct is None or total is None or total == 0:
        return jsonify({"error": "correct_count and total_count are required."}), 400

    lesson = db.session.get(Lesson, topic_id)
    if not lesson:
        return jsonify({"error": "Topic not found."}), 404

    score_pct = round((correct / total) * 100)
    mastered = score_pct >= MASTERY_THRESHOLD

    progress = _get_or_create_progress(user_id, topic_id)
    progress.practice_score = score_pct
    progress.attempt_count += 1
    progress.last_accessed = datetime.now(timezone.utc)

    if mastered:
        progress.status = "mastered"
    elif progress.status == "not_started":
        progress.status = "studied"

    db.session.commit()

    # Check if all 9 topics are mastered (for completion badge)
    all_progress = UserProgress.query.filter_by(user_id=user_id).all()
    from app.models import Lesson as LessonModel
    total_topics = LessonModel.query.count()
    mastered_count = sum(1 for p in all_progress if p.status == "mastered")
    all_complete = mastered_count == total_topics and total_topics > 0

    return jsonify({
        "score": score_pct,
        "correct": correct,
        "total": total,
        "mastered": mastered,
        "status": progress.status,
        "all_topics_complete": all_complete,
        "message": (
            "Well done! Topic mastered! 🎉" if mastered
            else f"You scored {score_pct}%. Review the lesson and try again to master this topic."
        ),
    }), 200
