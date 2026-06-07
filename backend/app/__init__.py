from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(
        app,
        origins=[
            "https://ai-python-tutor-web.vercel.app",   # Flutter web (prod)
            "http://localhost:*",                        # local Flutter/dev
            "http://127.0.0.1:*",
        ],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    # Import models so SQLAlchemy registers them (required before db.create_all)
    from app.models import User, Lesson, PracticeQuestion, UserProgress, ChatLog  # noqa: F401

    # Initialize Hybrid AI Rule Engine
    from app.engine import rule_engine
    rule_engine.load()

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.lessons import lessons_bp
    from app.routes.practice import practice_bp
    from app.routes.chat import chat_bp
    from app.routes.progress import progress_bp
    from app.routes.run_code import run_code_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(lessons_bp, url_prefix="/api/v1/lessons")
    app.register_blueprint(practice_bp, url_prefix="/api/v1/practice")
    app.register_blueprint(chat_bp, url_prefix="/api/v1/chat")
    app.register_blueprint(progress_bp, url_prefix="/api/v1/progress")
    app.register_blueprint(run_code_bp, url_prefix="/api/v1/run_code")

    return app
