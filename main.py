from fastapi import FastAPI
from service.read_calander import read_notion_database

app = FastAPI()


@app.get("/")
async def scan_calendar():
    data = read_notion_database()
    return data