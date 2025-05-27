from db.base import Base
from db.session import engine
from flask import Blueprint, jsonify
from sqlalchemy import text
from models.user import User
from models.arena import Arena
from models.activity import Activity
from models.arena_taken import ArenaTaken
from models.ticket import Ticket

dev_bp = Blueprint("dev", __name__, url_prefix="/dev")

@dev_bp.route("/create_all", methods=["POST"])
def create_all_tables():
    try:
        Base.metadata.create_all(bind=engine)
        return jsonify({"message": "All tables created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dev_bp.route("/drop_all", methods=["DELETE"])
def drop_all_tables():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """))
            tables = [row[0] for row in result]

            for table in tables:
                conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE;'))

            conn.commit()

        return jsonify({"message": "All tables dropped with CASCADE"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500