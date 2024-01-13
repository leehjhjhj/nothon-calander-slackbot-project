from entity import NotionPage
from database import get_db

class MeetingRepository:

    def add_meeting(self, meeting):
        with get_db() as db:
            db.add(meeting)
            db.commit()

    def merge_meeting(self, meeting):
        with get_db() as db:
            db.merge(meeting)
            db.commit()

    def get_all_page_ids(self, notion_database_id):
        with get_db() as db:
            return [m.page_id for m in db.query(NotionPage).filter_by(notion_database_id=notion_database_id)]
    
    def find_meeting_by_page_id(self, page_id) -> NotionPage:
        with get_db() as db:
            result = db.query(NotionPage).filter_by(page_id=page_id).first()
            return result
    
    