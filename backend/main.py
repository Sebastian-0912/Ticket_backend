from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify, abort, g
import os
from schemas.user import UserRole
from db.session import SessionLocal
from typing import cast
from api.auth import auth_bp
from api.dev import dev_bp
from api.arenas import arena_bp
from db.utils import get_db

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "secret")

# This runs before each request
@app.before_request
def create_db_session():
    g.db = SessionLocal()

# This runs after each request (even if error)
@app.teardown_request
def close_db_session(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def root():
    return jsonify({"message": "Flask ORM App is running!"})

# --- 資料庫連線測試端點 ---
@app.route("/db-test/")
def test_db_connection():
    db = get_db()
    try:
        # 執行一個簡單的查詢
        result = db.execute(text("SELECT * from users;"))
        return jsonify({"status": "success", "message": f"Database connection successful.{result}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database connection failed: {str(e)}"}), 500
    
app.register_blueprint(dev_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(arena_bp)