from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify, abort, g
import os
from schemas.user import UserRole
from db.session import SessionLocal
from typing import cast
from api.auth import auth_bp
from api.dev import dev_bp
from api.arenas import arena_bp
from api.activities import activities_bp
from api.tickets import tickets_bp
from db.utils import get_db
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "secret")
CORS(app, supports_credentials=True, origins="*")

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app, path='/metrics')

# Create a custom metric to track Flask instances
from prometheus_client import Gauge
flask_instance_gauge = Gauge('flask_instances_total', 'Total number of Flask instances', ['instance_name'])

# Register this instance
instance_name = os.getenv('FLASK_INSTANCE_NAME', 'flask_app_unknown')
flask_instance_gauge.labels(instance_name=instance_name).set(1)



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
app.register_blueprint(activities_bp)
app.register_blueprint(tickets_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
