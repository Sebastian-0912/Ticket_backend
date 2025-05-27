from flask import Blueprint, request, jsonify
from db.utils import get_db
from crud.tickets import (
    reserve_ticket,
    buy_ticket,
    refund_ticket,
    get_ticket_by_id,
    get_tickets_by_user
)
from utils.jwt_utils import jwt_required

tickets_bp = Blueprint("ticket", __name__, url_prefix="/tickets")

@tickets_bp.route("/reserve", methods=["POST"])
def reserve():
    db = get_db()
    data = request.json
    if not all(k in data for k in ("user_id", "activity_id", "num_tickets")):
        return "Invalid data", 400

    try:
        @jwt_required(db)
        def inner(user):
            ticket = reserve_tickets(db, data["user_id"], data["activity_id"], data["num_tickets"])
            if not ticket:
                return "Tickets sold out or invalid data", 400
            return jsonify({
                "id": str(ticket.id),
                "user_id": str(ticket.user_id),
                "activity_id": str(ticket.activity_id),
                "status": ticket.status,
                "reserved_at": ticket.reserved_at.isoformat()
            }), 201
        return inner()
    except Exception:
        return "Internal server error", 500

@tickets_bp.route("/buy", methods=["POST"])
def buy():
    db = get_db()
    data = request.json
    if "ticket_id" not in data:
        return "Invalid data", 400

    try:
        @jwt_required(db)
        def inner(user):
            result = buy_ticket(db, data["ticket_id"])
            if result is None:
                return "Ticket not found", 404
            if result == "invalid_state":
                return "Ticket not in unpaid state", 400
            return jsonify({
                "id": str(result.id),
                "status": result.status,
                "bought_at": result.bought_at.isoformat()
            }), 200
        return inner()
    except Exception:
        return "Internal server error", 500

@tickets_bp.route("/refund", methods=["POST"])
def refund():
    db = get_db()
    data = request.json
    if "ticket_id" not in data:
        return "Invalid data", 400

    try:
        @jwt_required(db)
        def inner(user):
            result = refund_ticket(db, data["ticket_id"])
            if result is None:
                return "Ticket not found", 404
            if result == "invalid_state":
                return "Ticket already used or cannot refund", 400
            return jsonify({
                "id": str(result.id),
                "status": result.status,
                "refunded_at": result.refunded_at.isoformat()
            }), 200
        return inner()
    except Exception:
        return "Internal server error", 500

@tickets_bp.route("/<ticket_id>", methods=["GET"])
def get_by_id(ticket_id):
    db = get_db()
    try:
        @jwt_required(db)
        def inner(user):
            ticket = get_ticket_by_id(db, ticket_id)
            if not ticket:
                return "Ticket not found", 404
            return jsonify({
                "id": str(ticket.id),
                "user_id": str(ticket.user_id),
                "activity_id": str(ticket.activity_id),
                "status": ticket.status,
                "reserved_at": ticket.reserved_at.isoformat() if ticket.reserved_at else None,
                "bought_at": ticket.bought_at.isoformat() if ticket.bought_at else None,
                "refunded_at": ticket.refunded_at.isoformat() if ticket.refunded_at else None
            }), 200
        return inner()
    except Exception:
        return "Internal server error", 500

@tickets_bp.route("/list_tickets", methods=["GET"])
def list_by_user():
    db = get_db()
    try:
        @jwt_required(db)
        def inner(user):
            tickets = get_tickets_by_user(db, user.id)
            return jsonify([
                {
                    "id": str(t.id),
                    "activity_id": str(t.activity_id),
                    "status": t.status,
                    "reserved_at": t.reserved_at.isoformat() if t.reserved_at else None,
                    "bought_at": t.bought_at.isoformat() if t.bought_at else None,
                    "refunded_at": t.refunded_at.isoformat() if t.refunded_at else None
                } for t in tickets
            ]), 200
        return inner()
    except Exception:
        return "Internal server error", 500
