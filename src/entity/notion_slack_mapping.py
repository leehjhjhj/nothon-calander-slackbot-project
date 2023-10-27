from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship

class NotionSlackMapping(Base):
    __tablename__ = "notion_slack_mapping"

    id = Column(Integer, primary_key=True)
    notion_database_id = Column(String(256), ForeignKey("notion_database.notion_database_id"))
    slack_channel_id = Column(String(256), ForeignKey("slack_channel.slack_channel_id"))
    connect_name = Column(String(64), nullable=False)

    notion_mapping = relationship("NotionDatabase", back_populates="notion_mappings")
    slack_mapping = relationship("SlackChannel", back_populates="slack_mappings")