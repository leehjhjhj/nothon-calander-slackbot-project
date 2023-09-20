from .read_calander import read_database
from .farthing import farthing_calender_data
from persistance.meeting_repository import MeetingRepository
from database import SessionLocal

repo = MeetingRepository(db=SessionLocal())

def save_meeting_facade():
    data = read_database()
    results = data.get('results')
    for result in results:
        meeting = farthing_calender_data(result)
        try:
            repo.save_meeting(meeting)
        except:
            print("저장 오류")

