from flask import Blueprint, jsonify, request

from app.services.auth_service import authenticate_user, generate_auth_token, serialize_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or data.get("email") or "").strip()
    password = data.get("password") or ""

    if not username:
        return jsonify({"error": "Username or email is required"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = authenticate_user(username, password)

    if not user:
        return jsonify({"error": "Invalid username/email or password"}), 401

    token = generate_auth_token(user)

    return jsonify(
        {
            "message": "Login successful",
            "token": token,
            "user": serialize_user(user),
        }
    )
