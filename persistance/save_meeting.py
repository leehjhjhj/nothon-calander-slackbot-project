from sqlalchemy.orm import Session


class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_meeting(self, meeting):
        self.db.add(meeting)
        self.db.commit()