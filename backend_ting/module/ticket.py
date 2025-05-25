import uuid
from datetime import datetime, timedelta
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, ForeignKey
from db.base_class import GUID, Base
from sqlalchemy.dialects.postgresql import UUID
from schemas.ticket import TicketStatus

# 定義 model
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    create_at = Column(DateTime, default=datetime.utcnow)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    seat_number = Column(String, unique=True)
    status = Column(String, Enum(TicketStatus),nullable=False)
    is_finish = Column(Boolean)
    