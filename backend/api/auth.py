from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from crud.user import get_user_by_email, create_user, verify_user_password
from utils.jwt_utils import create_access_token, jwt_required
from db.utils import get_db  # You need to define get_db to return a SQLAlchemy session

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/", methods=["POST"])
def register():
    db = get_db()
    data = request.json
    if get_user_by_email(db, data["email"]):
        return "Email or username already exists", 409
    user = create_user(db, data)
    return jsonify({
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "phone_number": user.phone_number
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.json
    user = get_user_by_email(db, data["email"])
    if not user or not verify_user_password(user, data["password"]):
        return "Invalid credentials", 401
    token = create_access_token(user.id)
    return jsonify({"access_token": token, "token_type": "bearer"})

@auth_bp.route("/get_user_info", methods=["GET"])
def get_user_info():
    db = get_db()
    @jwt_required(db)
    def inner(user):
        return jsonify({
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "phone_number": user.phone_number
        })
    return inner()

@auth_bp.route("/", methods=["PUT"])
def update_user():
    db = get_db()
    @jwt_required(db)
    def inner(user):
        data = request.json
        if "username" in data:
            user.username = data["username"]
        if "phone_number" in data:
            user.phone_number = data["phone_number"]
        db.commit()
        return jsonify({"message": "User updated successfully"})
    return inner()
