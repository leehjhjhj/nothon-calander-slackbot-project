from .read_calander import read_database
from .farthing import farthing_calender_data
from persistance.save_meeting import MeetingRepository
from database import SessionLocal

repo = MeetingRepository(db=SessionLocal())

def save_meeting_facade():
    data = read_database()
    results = data.get('results')
    for result in results:
        meeting = farthing_calender_data(result)
        repo.save_meeting(meeting)


