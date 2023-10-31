from sqlalchemy.orm import Session
from entity import SlackChannel, Slack, NotionDatabase, NotionSlackMapping
from sqlalchemy.orm import joinedload

class SlackRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_slack_channel_id_by_notion_database_id(self, notion_database_id):
        return self.db.query(NotionSlackMapping.slack_channel_id).filter_by(notion_database_id=notion_database_id).scalar()

    def get_api_token_by_slack_channel_id(self, slack_channel_id):
        slack_channel = (
            self.db.query(SlackChannel)
            .options(joinedload(SlackChannel.slack))
            .filter_by(slack_channel_id=slack_channel_id)
            .first()
        )

        if slack_channel and slack_channel.slack:
            return slack_channel.slack.slack_api_token
        else:
            return None
        
    def get_api_token_by_notion_database_id(self, notion_database_id):
        result = self.db.query(Slack.slack_api_token).\
        join(SlackChannel).\
        join(NotionSlackMapping).\
        join(NotionDatabase).\
        filter(NotionDatabase.notion_database_id == notion_database_id).\
        first()

        if result:
            return result[0]

        return None