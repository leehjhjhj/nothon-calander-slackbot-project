from fastapi import FastAPI, Depends
from service.read_calander import read_database
from decouple import config
from service.save_meeting_facade import save_meeting_facade
app = FastAPI()


@app.get("/")
async def scan_calendar():
    save_meeting_facade()
    return True