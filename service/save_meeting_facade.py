from .read_calander import read_notion_database
from .farthing import farthing_calender_data
from .check_meeting_id import check_meeting_id
from .worker_facade_service import worker_facade
from persistance.meeting_repository import MeetingRepository
from database import SessionLocal

repo = MeetingRepository(db=SessionLocal())

def save_meeting_facade():
    data = read_notion_database()
    results = data.get('results')
    list_meeting_ids = repo.get_all_meeting_ids()
    set_meeting_ids = set(list_meeting_ids)
    for result in results:
        meeting = farthing_calender_data(result)
        if check_meeting_id(meeting.page_id, set_meeting_ids):
            try:
                repo.merge_meeting(meeting)
            except:
                print("저장 오류")
        else:
            worker_facade(meeting)
            repo.add_meeting(meeting)