from app import db
from app.models import UserProgress


def get_or_create_progress(user_id: str, topic_id: str) -> UserProgress:
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
