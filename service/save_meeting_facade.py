from .read_calander import read_notion_database
from .farthing import farthing_calender_data
from .worker_facade_service import worker_facade
from .check_meeting import check_meeting_id, check_meeting_time

from persistance.meeting_repository import MeetingRepository
from persistance.notion_slack_mapping_repository import NotionSlackMappingRepository
from database import SessionLocal

meeting_repo = MeetingRepository(db=SessionLocal())
notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())

def save_meeting_facade():
    try:
        notion_database_ids = notion_slack_mapping_repo.get_all_database_ids()

        for notion_database_id in notion_database_ids:
            data = read_notion_database(notion_database_id)
            results = data.get('results')

            list_meeting_ids = meeting_repo.get_all_meeting_ids(notion_database_id)
            set_meeting_ids = set(list_meeting_ids)

            for result in results:
                meeting = farthing_calender_data(result)
                if check_meeting_time(meeting.time):
                    if check_meeting_id(meeting.page_id, set_meeting_ids):
                        try:
                            meeting_repo.merge_meeting(meeting)
                        except Exception as e:
                            print(f"저장 오류: {e}")
                    else:
                        worker_facade(meeting)
                        try:
                            meeting_repo.add_meeting(meeting)
                        except Exception as e:
                            print(f"저장 오류: {e}")
    finally:
        meeting_repo.db.close()
        notion_slack_mapping_repo.db.close()