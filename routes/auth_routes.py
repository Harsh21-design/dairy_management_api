from flask import Blueprint, request, jsonify
from extensions import db
from models.users import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from datetime import timedelta

auth = Blueprint("auth", __name__)

@auth.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "operator").strip().lower()
    full_name = data.get("full_name", "").strip()

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"}), 400

    if role not in ["admin", "operator", "viewer"]:
        role = "operator"

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409

    user = User(
        username=username,
        role=role,
        full_name=full_name or username,
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201

@auth.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    if not user.is_active:
        return jsonify({"message": "User account is disabled"}), 403

    # Additional claims inside token (role, full_name, user_id)
    additional_claims = {
        "user_id": user.id,
        "role": user.role,
        "full_name": user.full_name or user.username,
    }

    access_token = create_access_token(
        identity=str(user.username),
        additional_claims=additional_claims,
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@auth.route("/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_username = get_jwt_identity()
    claims = get_jwt()
    user = User.query.filter_by(username=current_username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user": user.to_dict(),
        "token_claims": claims
    }), 200

@auth.route("/auth/users", methods=["GET"])
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Admin privileges required"}), 403

    users = User.query.order_by(User.id.asc()).all()
    return jsonify({
        "users": [u.to_dict() for u in users]
    }), 200
