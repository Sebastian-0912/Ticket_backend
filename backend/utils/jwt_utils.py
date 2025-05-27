import jwt
from datetime import datetime, timedelta
from flask import current_app
from functools import wraps
from flask import request, jsonify
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserRole


def create_access_token(user_id, expires_delta=timedelta(hours=2)):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + expires_delta
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(db: Session):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", None)
            if not auth or not auth.startswith("Bearer "):
                return "Unauthorized", 401
            token = auth.split(" ")[1]
            user_id = decode_token(token)
            if not user_id:
                return "Unauthorized", 401
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return "Unauthorized", 401
            return f(user, *args, **kwargs)
        return wrapper
    return decorator


def host_required(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if user.role != UserRole.HOST:
            return "Forbidden: Host access required", 403
        return func(user, *args, **kwargs)
    return wrapper