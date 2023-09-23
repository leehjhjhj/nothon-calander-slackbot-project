from fastapi import FastAPI
from service.read_calander import read_notion_database
from database import SessionLocal
from persistance.notion_slack_mapping_repository import NotionSlackMappingRepository

notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())

app = FastAPI()


@app.get("/")
async def scan_calendar():
    notion_database_ids = notion_slack_mapping_repo.get_all_database_ids()

    for notion_database_id in notion_database_ids:
        data = read_notion_database(notion_database_id)
    return data