from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from src.database import Base
from datetime import datetime
import enum
from sqlalchemy.orm import relationship

class StatusChoice(enum.Enum):
    CONFIRMED = "확정"
    CANCELLED = "취소 및 변경"

class Notion(Base):
    __tablename__ = "notion"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    notion_api_token = Column(String(256), nullable=False)

    notion_databases = relationship("NotionDatabase", back_populates="notion", cascade="all, delete-orphan")

class NotionDatabase(Base):
    __tablename__ = "notion_database"

    notion_database_id = Column(String(256), primary_key=True)
    notion_id = Column(Integer, ForeignKey('notion.id'))
    db_name = Column(String(64), nullable=False)

    notion = relationship("Notion", back_populates="notion_databases")
    notion_pages = relationship("NotionPage", back_populates="notion_database", cascade="all, delete-orphan")
    notion_mappings = relationship("NotionSlackMapping", back_populates="notion_mapping", cascade="all, delete-orphan")

class NotionPage(Base):
    __tablename__ = "notion_page"

    page_id = Column(String(128), primary_key=True)
    notion_database_id = Column(String(256), ForeignKey("notion_database.notion_database_id"))
    status = Column(Enum(StatusChoice), nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    meeting_type = Column(String(64), nullable=False)
    meeting_url = Column(String(512), nullable=False)
    name = Column(String(64), nullable=False)

    notion_database = relationship("NotionDatabase", back_populates="notion_pages")