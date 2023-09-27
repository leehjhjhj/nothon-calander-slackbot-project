from persistance.meeting_repository import MeetingRepository
from database import SessionLocal
from entity import StatusChoice

def check_status(page_id: str):
    repo = MeetingRepository(db=SessionLocal())
    try:
        notion = repo.find_meeting_by_page_id(page_id)
        if notion.status == StatusChoice.CANCELLED:
            return False
        
        return True
    finally:
        repo.db.close()