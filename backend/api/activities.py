from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from utils.jwt_utils import jwt_required, host_required
from db.utils import get_db
from crud.arenas import get_arena_by_id
from crud.activities import (
    create_activity,
    get_activity_by_id,
    get_all_activities,
    get_activities_by_creator,
    update_activity,
    is_arena_available,
    create_arena_taken,
)
from crud.tickets import get_tickets_by_user

activities_bp = Blueprint("activities", __name__, url_prefix="/activities")


def activity_to_dict(activity):
    return {
        "id": str(activity.id),
        "title": activity.title,
        "content": activity.content,
        "price": activity.price,
        "on_sale_date": activity.on_sale_date.isoformat() if activity.on_sale_date else None,
        "start_time": activity.start_time.isoformat() if activity.start_time else None,
        "end_time": activity.end_time.isoformat() if activity.end_time else None,
        "cover_image": activity.cover_image,
        "arena_id": str(activity.arena_id),
        "creator_id": str(activity.creator_id),
        "num_ticket": activity.num_ticket,
        "is_achieved": activity.is_achieved,
    }


@activities_bp.route("/", methods=["POST"])
def create():
    db: Session = get_db()
    data = request.json
    required_fields = ["title", "content", "price", "on_sale_date", "start_time", "end_time", "cover_image", "arena_id"]
    if not all(k in data for k in required_fields):
        return "Invalid data", 400

    try:
        @jwt_required(db)
        @host_required
        def inner(user):
            try:
                on_sale_date = datetime.fromisoformat(data["on_sale_date"])
                start_time = datetime.fromisoformat(data["start_time"])
                end_time = datetime.fromisoformat(data["end_time"])
                price = int(data["price"])
                arena_uuid = uuid.UUID(data["arena_id"])
            except Exception:
                return "Invalid date or price format", 400

            arena = get_arena_by_id(db, arena_uuid)
            if not arena:
                return "Arena not found", 400

            if not is_arena_available(db, arena.id, start_time.date()):
                return "Arena is already taken for this date", 400

            activity = create_activity(
                db,
                title=data["title"],
                content=data["content"],
                price=price,
                on_sale_date=on_sale_date,
                start_time=start_time,
                end_time=end_time,
                cover_image=data["cover_image"],
                arena_id=arena.id,
                creator_id=user.id,
                num_ticket=arena.capacity,
            )

            create_arena_taken(db, activity.id, arena.id, start_time.date())
            # Create tickets for activity
            from crud.tickets import create_tickets_for_activity

            create_tickets_for_activity(db, activity.id, arena.capacity)
            db.commit()

            return jsonify(activity_to_dict(activity)), 201

        return inner()
    except Exception:
        return "Internal server error", 500


@activities_bp.route("/", methods=["GET"])
def get_all():
    db: Session = get_db()
    try:
        activities = get_all_activities(db)
        result = [activity_to_dict(act) for act in activities]
        return jsonify(result), 200
    except Exception:
        return "Internal server error", 500


@activities_bp.route("/<string:activity_id>", methods=["GET"])
def get_one(activity_id):
    db: Session = get_db()
    try:
        try:
            act_uuid = uuid.UUID(activity_id)
        except Exception:
            return "Activity not found", 404

        activity = get_activity_by_id(db, act_uuid)
        if not activity:
            return "Activity not found", 404

        return jsonify(activity_to_dict(activity)), 200
    except Exception:
        return "Internal server error", 500


@activities_bp.route("/<string:activity_id>", methods=["PUT"])
def update(activity_id):
    db: Session = get_db()
    data = request.json
    allowed_keys = ["title", "content", "price", "on_sale_date", "start_time", "end_time", "cover_image"]
    update_data = {k: v for k, v in data.items() if k in allowed_keys}

    if not update_data:
        return "Invalid data", 400

    try:
        @jwt_required(db)
        @host_required
        def inner(user):
            try:
                act_uuid = uuid.UUID(activity_id)
            except Exception:
                return "Activity not found", 404

            activity = get_activity_by_id(db, act_uuid)
            if not activity:
                return "Activity not found", 404

            # Only creator can update
            if activity.creator_id != user.id:
                return "Unauthorized", 401

            # If dates or price provided, convert them properly
            if "price" in update_data:
                try:
                    update_data["price"] = int(update_data["price"])
                except Exception:
                    return "Invalid price format", 400
            for date_field in ["on_sale_date", "start_time", "end_time"]:
                if date_field in update_data:
                    try:
                        update_data[date_field] = datetime.fromisoformat(update_data[date_field])
                    except Exception:
                        return f"Invalid {date_field} format", 400

            update_activity(db, activity, update_data)
            return jsonify({"message": "Activity updated successfully"}), 200

        return inner()
    except Exception:
        return "Internal server error", 500


@activities_bp.route("/list_activities/host", methods=["GET"])
def list_activities_host():
    db: Session = get_db()
    try:
        @jwt_required(db)
        @host_required
        def inner(user):
            activities = get_activities_by_creator(db, user.id)
            result = [activity_to_dict(act) for act in activities]
            return jsonify(result), 200

        return inner()
    except Exception:
        return "Internal server error", 500


@activities_bp.route("/list_activities/client", methods=["GET"])
def list_activities_client():
    db: Session = get_db()
    try:
        @jwt_required(db)
        def inner(user):
            from crud.tickets import get_tickets_by_user

            tickets = get_tickets_by_user(db, user.id)
            activity_ids = {t.activity_id for t in tickets}
            activities = [get_activity_by_id(db, aid) for aid in activity_ids if aid]
            activities = [act for act in activities if act]
            result = [activity_to_dict(act) for act in activities]
            return jsonify(result), 200

        return inner()
    except Exception:
        return "Internal server error", 500
