from sqlalchemy.orm import Session
from entity import SlackChannel, Slack
from sqlalchemy.orm import joinedload

class SlackRepository:
    
    def __init__(self, db: Session):
        self.db = db

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