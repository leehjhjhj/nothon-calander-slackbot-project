import json
from .scrum_dto import ScrumRequestDto
from datetime import datetime, timedelta, time as make_time
import pytz
from aiohttp import ClientSession

class ScrumProcess:
    def __init__(self, request_data: ScrumRequestDto):
        self.__api_key = request_data.notion_api_key
        self._database_id = request_data.notion_database_id

    async def create_scrum_in_notion(self, request_data: ScrumRequestDto):
        headers, page_data = self._make_post(request_data)
        async with ClientSession() as session:
            async with session.post('https://api.notion.com/v1/pages', headers=headers, data=json.dumps(page_data)) as response:
                return await response.json()
    
    def _make_post(self, request_data: ScrumRequestDto):
        headers = {
            "Authorization": "Bearer " + self.__api_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }
        page_data = {
        "parent": {"database_id": self._database_id},
        "children": self._make_block(),
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
                        "name": "전체"
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
        return headers, page_data


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
    
    def _make_block(self):
        parts = ('기획', '관객 서버', '매니저 서버', '클라이언트', '디자인')
        parts_block = [
            {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                {
                    "type": "text",
                    "text": { "content": part }
                }
                ]
            }
        }
            for part in parts
        ]

        return [
            {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                {
                    "type": "text",
                    "text": { "content": "파트별 진행 상황 공유" }
                }
                ]
            }
        }] + parts_block + [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                {
                    "type": "text",
                    "text": { "content": "회고" }
                }
                ]
            }
        }] + [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                {
                    "type": "text",
                    "text": { "content": "다음 스프린트 목표" }
                }
                ]
            }
        }] + parts_block 