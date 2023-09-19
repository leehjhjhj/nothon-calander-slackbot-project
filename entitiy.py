from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
from datetime import datetime
import enum

class StatusChoice(enum.Enum):
    CONFIRMED = "확정"
    CANCELLED = "취소 및 변경"

class Notion(Base):
    __tablename__ = "notion"

    id = Column(Integer, primary_key=True)
    page_id = Column(String(128), nullable=False)
    status = Column(Enum(StatusChoice), nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    meeting_type = Column(String(64), nullable=False)
    meeting_url = Column(String(512), nullable=False)
    name = Column(String(64), nullable=False)