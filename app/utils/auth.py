from functools import wraps

import jwt
from flask import g, jsonify, request

from app.services.auth_service import verify_auth_token


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token is required"}), 401

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({"error": "Authorization token is required"}), 401

        try:
            user = verify_auth_token(token)

            if not user:
                return jsonify({"error": "Invalid authentication token"}), 401

            g.current_user = user
            return fn(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Authentication token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token"}), 401

    return wrapper
