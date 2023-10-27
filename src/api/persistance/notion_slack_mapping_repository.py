from sqlalchemy.orm import Session
from entity import NotionSlackMapping

class NotionSlackMappingRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_all_database_ids(self):
        return [record[0] for record in self.db.query(NotionSlackMapping.notion_database_id).distinct().all()]
    
    def get_slack_channel_id_by_notion_database_id(self, notion_database_id):
        return [m.slack_channel_id for m in self.db.query(NotionSlackMapping).filter_by(notion_database_id=notion_database_id)] 