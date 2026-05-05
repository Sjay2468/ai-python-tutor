from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import datetime, timezone
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint("auth", __name__)


def _validate_register_payload(data):
    """Returns (error_message, None) or (None, cleaned_data)."""
    required = ["full_name", "email", "password", "skill_level"]
    for field in required:
        if not data.get(field):
            return f"'{field}' is required.", None

    if len(data["password"]) < 8:
        return "Password must be at least 8 characters.", None

    if data["skill_level"] not in ("none", "little", "some"):
        return "skill_level must be 'none', 'little', or 'some'.", None

    return None, data


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/v1/auth/register
    Register a new user account.
    Body: { full_name, email, password, skill_level }
    """
    data = request.get_json(silent=True) or {}

    error, _ = _validate_register_payload(data)
    if error:
        return jsonify({"error": error}), 400

    # Check email uniqueness
    if User.query.filter_by(email=data["email"].lower().strip()).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    # Hash password and save user
    pw_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        full_name=data["full_name"].strip(),
        email=data["email"].lower().strip(),
        password_hash=pw_hash,
        skill_level=data["skill_level"],
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/v1/auth/login
    Authenticate a user and return a JWT.
    Body: { email, password }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password."}), 401

    # Update last login timestamp
    user.last_login = datetime.now(timezone.utc)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    POST /api/v1/auth/logout
    Client-side logout — instructs client to delete the stored token.
    Note: For stateless JWT, full token blacklisting requires a blocklist store.
    """
    return jsonify({"message": "Logged out successfully. Please delete your local token."}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    GET /api/v1/auth/profile
    Return the authenticated user's profile.
    """
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    """
    PATCH /api/v1/auth/profile
    Update the authenticated user's full_name or skill_level.
    Body: { full_name?, skill_level? }
    """
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json(silent=True) or {}

    if "full_name" in data and data["full_name"].strip():
        user.full_name = data["full_name"].strip()

    if "skill_level" in data:
        if data["skill_level"] not in ("none", "little", "some"):
            return jsonify({"error": "skill_level must be 'none', 'little', or 'some'."}), 400
        user.skill_level = data["skill_level"]

    db.session.commit()
    return jsonify({"user": user.to_dict()}), 200
