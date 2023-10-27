from sqlalchemy.orm import Session
from entity import Notion, NotionDatabase
from sqlalchemy.orm import joinedload

class NotionRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_api_token_by_notion_database_id(self, notion_database_id):
        notion_database = (
            self.db.query(NotionDatabase)
            .options(joinedload(NotionDatabase.notion))
            .filter_by(notion_database_id=notion_database_id)
            .first()
        )

        if notion_database and notion_database.notion:
            return notion_database.notion.notion_api_token
        else:
            return None