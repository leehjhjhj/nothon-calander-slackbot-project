from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship


class Slack(Base):
    __tablename__ = "slack"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    slack_api_token = Column(String(256), nullable=False)

    slack_channels = relationship("SlackChannel", back_populates="slack", cascade="all, delete-orphan")

class SlackChannel(Base):
    __tablename__ = "slack_channel"

    slack_channel_id = Column(String(256), primary_key=True)
    slack_id = Column(Integer, ForeignKey("slack.id"))
    channel_name = Column(String(64), nullable=False)

    slack = relationship("Slack", back_populates="slack_channels")
    slack_mappings = relationship("NotionSlackMapping", back_populates="slack_mapping", cascade="all, delete-orphan")