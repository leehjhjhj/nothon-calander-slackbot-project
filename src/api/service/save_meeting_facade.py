from .worker_facade_service import worker_facade
from datetime import datetime, timedelta
from entity import NotionPage, StatusChoice
import logging
import requests
from pytz import timezone

class MeetingProcess:
    def __init__(self, meeting_repository, notion_slack_mapping_repository, notion_repository, participants_process):
        self._meeting_repo = meeting_repository
        self._notion_slack_mapping_repo = notion_slack_mapping_repository
        self._notion_repo = notion_repository
        self._participants_process = participants_process
        
    def save_meeting(self):
        try:
            notion_database_ids = self._notion_slack_mapping_repo.get_all_database_ids()
            for notion_database_id in notion_database_ids:
                notion_api_key = self._notion_repo.get_api_token_by_notion_database_id(notion_database_id)
                data = self._read_notion_database(notion_database_id, notion_api_key)
                results = data.get('results')
                
                list_meeting_ids = self._meeting_repo.get_all_page_ids(notion_database_id)
                set_meeting_ids = set(list_meeting_ids)

                for result in results:
                    try:
                        meeting = self._farthing_calender_data(result)
                        if not self._check_meeting_status(meeting.status):
                            continue
                        if self._check_meeting_time(meeting.time) and not self._check_meeting_id(meeting.page_id, set_meeting_ids):
                            logging.info(f"{meeting.name}이 if에 들어왔다.")
                            meeting = self._participants_process.add_participants(meeting, result)
                            worker_facade(meeting)
                            try:
                                self._meeting_repo.add_meeting(meeting)
                            except Exception as e:
                                logging.error(f"저장 오류: {e}")
                    except Exception as e:
                        logging.error("DB ID: {}, 파싱 에러 발생: {}".format(notion_database_id, e))
                        continue
        except Exception as e:
            logging.error(f"save meeting 자체 오류 발생!: {e}")

    def _read_notion_database(self, notion_database_id, notion_api_key):
        token = notion_api_key
        database_id = notion_database_id
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }
        readUrl = f"https://api.notion.com/v1/databases/{database_id}/query"
        res = requests.request("POST", readUrl, headers=headers)
        data = res.json()
        return data

    def _farthing_calender_data(self, result) -> NotionPage:
        properties = result.get('properties', {})

        status_str = properties.get("확정여부", {}).get("multi_select", [{}])[0].get("name")
        status_enum = StatusChoice(status_str) if status_str else None
        notion_database_id=result.get("parent",{}).get("database_id").replace('-','')

        meeting = NotionPage(
            page_id=result.get('id'),
            notion_database_id=notion_database_id,
            status=status_enum,
            time=datetime.fromisoformat(properties.get("날짜", {}).get("date", {}).get("start")),
            meeting_type=properties.get("종류", {}).get("multi_select", [{}])[0].get("name"),
            meeting_url=result.get('url'),
            name=properties.get("이름", {}).get("title", [{}])[0].get('text').get('content'),
        )
        return meeting

    def _check_meeting_status(self, status):
        if status == StatusChoice.CONFIRMED:
            return True
        return False

    def _check_meeting_id(self, target_id, meeting_ids):
        if target_id in meeting_ids:
            return True
        else:
            return False

    def _check_meeting_time(self, meeting_time):
        try:
            now = datetime.now(tz=timezone('Asia/Seoul'))
            day_after_tomorrow_start = (now + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
            if now <= meeting_time < day_after_tomorrow_start:
                return True
            return False
        except TypeError as e:
            if str(e) == "can't compare offset-naive and offset-aware datetimes":
                logging.error(f'시간 에러, 노션 DB 시간 수정 요망: {e}')
                return False