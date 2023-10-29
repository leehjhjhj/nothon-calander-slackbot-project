from .read_calander import read_notion_database
from .farthing import farthing_calender_data
from .worker_facade_service import worker_facade
from .check_meeting import check_meeting_id, check_meeting_time
from .add_participants import add_participants
from api.persistance.meeting_repository import MeetingRepository
from api.persistance.notion_slack_mapping_repository import NotionSlackMappingRepository
from api.persistance.notion_repository import NotionRepository
from database import SessionLocal
import logging

def save_meeting_facade():
    meeting_repo = MeetingRepository(db=SessionLocal())
    notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())
    notion_repo = NotionRepository(db=SessionLocal())

    try:
        notion_database_ids = notion_slack_mapping_repo.get_all_database_ids()
        logging.info("DB에 있는 노션디비 목록: %s", notion_database_ids)

        for notion_database_id in notion_database_ids:
            notion_api_key = notion_repo.get_api_token_by_notion_database_id(notion_database_id)
            data = read_notion_database(notion_database_id, notion_api_key)
            results = data.get('results')

            list_meeting_ids = meeting_repo.get_all_page_ids(notion_database_id)
            set_meeting_ids = set(list_meeting_ids)
            logging.info(f"DB에 있는 회의 목록 {set_meeting_ids}")

            for result in results:
                meeting = farthing_calender_data(result)
                if check_meeting_time(meeting.time):
                    if not check_meeting_id(meeting.page_id, set_meeting_ids):
                        logging.info(f"{meeting.name}이 ifif에 들어왔다.")
                        meeting = add_participants(meeting, result)
                        worker_facade(meeting)
                        try:
                            meeting_repo.add_meeting(meeting)
                        except Exception as e:
                            logging.error(f"저장 오류: {e}")

    except Exception as e:
        logging.error(f"save meeting 자체 오류 발생!: {e}")

    finally:
        meeting_repo.db.close()
        notion_slack_mapping_repo.db.close()
        notion_repo.db.close()