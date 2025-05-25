import uuid
from sqlalchemy import Date, Column, ForeignKey, ForeignKey
from db.base_class import GUID, Base
from sqlalchemy.dialects.postgresql import UUID


# 定義 model
class ArenaTaken(Base):
    __tablename__ = "arena_taken"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    arena_id = Column(UUID(as_uuid=True), ForeignKey("arenas.id"), nullable=False)
    date = Column(Date, nullable=False)
