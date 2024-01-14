from entity import Notion, NotionDatabase
from sqlalchemy.orm import joinedload
from database import get_db

class NotionRepository:

    def get_api_token_by_notion_database_id(self, notion_database_id):
        with get_db() as db:
            notion_database = (
                db.query(NotionDatabase)
                .options(joinedload(NotionDatabase.notion))
                .filter_by(notion_database_id=notion_database_id)
                .first()
            )

            if notion_database and notion_database.notion:
                return notion_database.notion.notion_api_token
            else:
                return None
            
    def find_notion_database_by_name_with_notion(self, db_name: str):
        with get_db() as db:
            return (
                db.query(NotionDatabase)
                .options(joinedload(NotionDatabase.notion))  # Notion 객체를 조인
                .filter(NotionDatabase.db_name == db_name)
                .one()
            )