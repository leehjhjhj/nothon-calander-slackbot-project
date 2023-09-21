from sqlalchemy.orm import Session
from entity import Notion

class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_meeting(self, meeting):
        self.db.add(meeting)
        self.db.commit()

    def merge_meeting(self, meeting):
        self.db.merge(meeting)
        self.db.commit()

    def get_all_meeting_ids(self):
       return [m.page_id for m in self.db.query(Notion).all()]
    
    def find_meeting_by_page_id(self, page_id):
        result = self.db.query(Notion).filter_by(page_id=page_id).first()
        return result