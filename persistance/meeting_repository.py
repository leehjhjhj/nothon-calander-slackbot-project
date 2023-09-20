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
       return [m.id for m in self.db.query(Notion).all()]