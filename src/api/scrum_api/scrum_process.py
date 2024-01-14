import json
from .scrum_dto import ScrumRequestDto
from datetime import datetime, timedelta, time as make_time
import pytz
from aiohttp import ClientSession
from .blocks.etc_blocks import *
from .blocks.text_blocks import *

class ScrumProcess:
    def __init__(self, notion_repository):
        self._notion_repository = notion_repository

    async def create_scrum_in_notion(self, request_data: ScrumRequestDto):
        headers, database_id = self._make_header(request_data.db_name)
        page_data = self._make_post(request_data, database_id)
        async with ClientSession() as session:
            async with session.post('https://api.notion.com/v1/pages', headers=headers, data=json.dumps(page_data)) as response:
                return await response.json()
            
    def _make_header(self, db_name: str):
        notion_database = self._notion_repository.find_notion_database_by_name_with_notion(db_name)
        api_key = notion_database.notion.notion_api_token
        database_id = notion_database.notion_database_id
        headers = {
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-02-22"
            }
        return headers, database_id

    def _make_post(self, request_data: ScrumRequestDto, database_id: str):
        page_data = {
        "parent": {"database_id": database_id},
        "children": request_data.blocks,
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": request_data.name,
                        }
                    }
                ]
            },
            "종류": {
                "multi_select": [
                    {
                        "name": request_data.type
                    }
                ]
            },
            "참여 파트": {
                "multi_select": [
                    {
                        "name": request_data.part
                    }
                ]
            },
            "확정여부": {
                "multi_select": [
                    {
                        "name": "미정"
                    }
                ]
            },
            "날짜": {
                "date": {
                    "start": self._make_date(request_data.day, request_data.time)
                }
            }
            }
        }
        return page_data


    def _make_date(self, day, time):
        day_to_weekday = {
            "월요일": 0,
            "화요일": 1,
            "수요일": 2,
            "목요일": 3,
            "금요일": 4,
            "토요일": 5,
            "일요일": 6
        }
        target_weekday = day_to_weekday[day]
    
        now = datetime.now(pytz.timezone('Asia/Seoul'))
        current_weekday = now.weekday()
        day_diff = (target_weekday - current_weekday + 7) % 7
        if day_diff == 0: 
            day_diff = 7

        target_date = now.date() + timedelta(days=day_diff)
        hour, minute = map(int, time.split(':')) 
        target_datetime = datetime.combine(target_date, make_time(hour=hour-9, minute=minute))
        return target_datetime.isoformat()