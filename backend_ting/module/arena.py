import uuid
from sqlalchemy import Column, String, Integer
from db.base_class import GUID, Base
from sqlalchemy.dialects.postgresql import UUID

# 定義 model
class Arena(Base):
    __tablename__ = "arenas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    address = Column(String)
    capacity = Column(Integer)