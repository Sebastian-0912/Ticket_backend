from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from crud.arenas import create_arena, get_all_arenas, get_arena_by_id
from utils.jwt_utils import jwt_required
from db.utils import get_db

arena_bp = Blueprint("arena", __name__, url_prefix="/arenas")

@arena_bp.route("/", methods=["POST"])
def create():
    db = get_db()
    data = request.json
    if not all(k in data for k in ("title", "address", "capacity")):
        return "Invalid data", 400
    try:
        @jwt_required(db)
        def inner(user):
            arena = create_arena(db, data["title"], data["address"], data["capacity"])
            return jsonify({
                "id": str(arena.id),
                "title": arena.title,
                "address": arena.address,
                "capacity": arena.capacity
            }), 201
        return inner()
    except Exception as e:
        return "Internal server error", 500

@arena_bp.route("/", methods=["GET"])
def get_all():
    db = get_db()
    try:
        arenas = get_all_arenas(db)
        return jsonify([
            {
                "id": str(a.id),
                "title": a.title,
                "address": a.address,
                "capacity": a.capacity
            } for a in arenas
        ])
    except Exception:
        return "Internal server error", 500

@arena_bp.route("/<arena_id>", methods=["GET"])
def get_by_id(arena_id):
    db = get_db()
    try:
        arena = get_arena_by_id(db, arena_id)
        if not arena:
            return "Arena not found", 404
        return jsonify({
            "id": str(arena.id),
            "title": arena.title,
            "address": arena.address,
            "capacity": arena.capacity
        })
    except Exception:
        return "Internal server error", 500
