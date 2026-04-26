from flask import Blueprint, jsonify, request

from app.services.motor_service import create_motors, get_all_motors
from app.utils.auth import auth_required

motor_bp = Blueprint("motor", __name__)


@motor_bp.route("/motors/generate", methods=["POST"])
@auth_required
def generate_motors():
    data = request.get_json() or {}
    total = data.get("total")
    genre = data.get("genre")

    if total is None:
        return jsonify({"error": "Total is required"}), 400

    if not isinstance(total, int):
        return jsonify({"error": "Total harus berupa angka"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_motors(total, genre)
        return jsonify(
            {
                "category": "modern trending motors",
                "total": len(result),
                "data": result,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motor_bp.route("/motors", methods=["GET"])
def get_motors():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    return jsonify(get_all_motors(page=page, per_page=per_page))
