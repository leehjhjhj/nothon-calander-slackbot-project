from entity import NotionSlackMapping
from database import get_db

class NotionSlackMappingRepository:

    def get_all_database_ids(self):
        with get_db() as db:
            return [record[0] for record in db.query(NotionSlackMapping.notion_database_id).distinct().all()]
    
    def get_slack_channel_id_by_notion_database_id(self, notion_database_id):
        with get_db() as db:
            return [m.slack_channel_id for m in db.query(NotionSlackMapping).filter_by(notion_database_id=notion_database_id)]
        
    def get_all_slack_channels(self):
        with get_db() as db:
            return [record[0] for record in db.query(NotionSlackMapping.slack_channel_id).distinct().all()]
      
    def get_slack_channel_id_by_notion_database_id(self, notion_database_id):
        with get_db() as db:
            return [m.slack_channel_id for m in db.query(NotionSlackMapping).filter_by(notion_database_id=notion_database_id)]
