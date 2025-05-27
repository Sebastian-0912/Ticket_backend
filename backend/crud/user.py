from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from datetime import datetime, timezone

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    hashed_pw = generate_password_hash(user_data["password"])
    user = User(
        email=user_data["email"],
        username=user_data["username"],
        password=hashed_pw,
        role=user_data["role"],
        phone_number=user_data["phone_number"],
        create_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_user_password(user: User, password: str):
    return check_password_hash(user.password, password)
