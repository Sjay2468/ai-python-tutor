import uuid
from datetime import datetime, timezone
from app import db


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    """Stores registered user accounts."""
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    skill_level = db.Column(
        db.Enum("none", "little", "some", name="skill_level_enum"),
        nullable=False,
        default="none",
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    progress = db.relationship("UserProgress", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "skill_level": self.skill_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Lesson(db.Model):
    """Stores the 9 beginner Python lesson topics."""
    __tablename__ = "lessons"

    id = db.Column(db.String(10), primary_key=True)   # e.g. "L01"
    title = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    analogy = db.Column(db.Text, nullable=True)        # Real-world analogy
    code_example = db.Column(db.Text, nullable=False)
    code_breakdown = db.Column(db.Text, nullable=True) # Line-by-line explanation
    key_points = db.Column(db.Text, nullable=False)    # Stored as JSON string
    order_index = db.Column(db.Integer, nullable=False, unique=True)
    difficulty = db.Column(db.String(20), nullable=False, default="beginner")

    # Relationships
    questions = db.relationship("PracticeQuestion", backref="lesson", lazy=True)
    progress_records = db.relationship("UserProgress", backref="lesson", lazy=True)

    def to_dict(self, status=None):
        return {
            "id": self.id,
            "title": self.title,
            "order_index": self.order_index,
            "difficulty": self.difficulty,
            "status": status or "not_started",
        }

    def to_full_dict(self, status=None, score=None):
        import json
        return {
            "id": self.id,
            "title": self.title,
            "explanation": self.explanation,
            "analogy": self.analogy,
            "code_example": self.code_example,
            "code_breakdown": self.code_breakdown,
            "key_points": json.loads(self.key_points) if self.key_points else [],
            "order_index": self.order_index,
            "difficulty": self.difficulty,
            "status": status or "not_started",
            "practice_score": score,
        }


class PracticeQuestion(db.Model):
    """Multiple-choice practice questions with progressive hints."""
    __tablename__ = "practice_questions"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    topic_id = db.Column(db.String(10), db.ForeignKey("lessons.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(
        db.Enum("A", "B", "C", "D", name="option_enum"),
        nullable=False,
    )
    hint_1 = db.Column(db.Text, nullable=False)   # General nudge
    hint_2 = db.Column(db.Text, nullable=False)   # More specific clue
    hint_3 = db.Column(db.Text, nullable=False)   # Reveal reasoning + answer

    def to_dict(self):
        """Return question without revealing the correct answer."""
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "question_text": self.question_text,
            "options": {
                "A": self.option_a,
                "B": self.option_b,
                "C": self.option_c,
                "D": self.option_d,
            },
        }


class UserProgress(db.Model):
    """Tracks per-user, per-topic study and mastery status."""
    __tablename__ = "user_progress"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.String(10), db.ForeignKey("lessons.id"), nullable=False)
    status = db.Column(
        db.Enum("not_started", "studied", "mastered", name="progress_status_enum"),
        nullable=False,
        default="not_started",
    )
    practice_score = db.Column(db.Integer, nullable=True)  # 0-100 (%)
    last_accessed = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    attempt_count = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),
    )

    def to_dict(self):
        return {
            "topic_id": self.topic_id,
            "status": self.status,
            "practice_score": self.practice_score,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "attempt_count": self.attempt_count,
        }


class ChatLog(db.Model):
    """Analytics log for each hybrid controller query — NO user query text stored."""
    __tablename__ = "chat_logs"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id_hash = db.Column(db.String(64), nullable=False)   # SHA-256 hash, not reversible
    topic_context = db.Column(db.String(10), nullable=True)
    intent_category = db.Column(
        db.Enum(
            "concept_question", "hint_request", "error_explanation", "out_of_scope",
            name="intent_enum",
        ),
        nullable=True,
    )
    response_source = db.Column(
        db.Enum("rule_based", "nlp_grounded", "nlp_only", "fallback", name="source_enum"),
        nullable=True,
    )
    latency_ms = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
