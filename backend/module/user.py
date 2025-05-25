import uuid
from sqlalchemy import Column, DateTime, Enum, String
from db.base_class import GUID, Base
from sqlalchemy.dialects.postgresql import UUID
from schemas.user import UserRole

# 定義 model
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    role = Column(String, Enum(UserRole),nullable=False)
    phone_number = Column(String)
    create_at = Column(DateTime)



