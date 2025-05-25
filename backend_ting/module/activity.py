import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, ForeignKey, Integer
from db.base_class import GUID, Base
from sqlalchemy.dialects.postgresql import UUID

# 定義 model
# ForeignKey() 只能指向另一個資料表的「主鍵（通常是 id）」或「唯一鍵」，不能指向普通欄位（像 capacity）
class Activity(Base):
    __tablename__ = "activities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = Column(Integer)
    on_sale_date = Column(DateTime)
    num_ticket = Column(Integer, nullable=False, default=0)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    title = Column(String)
    content = Column(String)
    cover_image = Column(String)
    arena_id = Column(UUID(as_uuid=True), ForeignKey("arenas.id"), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_achieved = Column(Boolean)
