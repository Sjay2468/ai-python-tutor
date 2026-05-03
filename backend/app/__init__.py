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
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.lessons import lessons_bp
    from app.routes.practice import practice_bp
    from app.routes.chat import chat_bp
    from app.routes.progress import progress_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(lessons_bp, url_prefix="/api/v1/lessons")
    app.register_blueprint(practice_bp, url_prefix="/api/v1/practice")
    app.register_blueprint(chat_bp, url_prefix="/api/v1")
    app.register_blueprint(progress_bp, url_prefix="/api/v1/progress")

    return app
