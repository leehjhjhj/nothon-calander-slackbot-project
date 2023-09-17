from fastapi import FastAPI, Depends
from test import read_database
from decouple import config

app = FastAPI()

token = config('NOTION_TOKEN')
database_id = config('NOTION_DATABASE_ID')
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

@app.get("/")
async def root():
    res = read_database(database_id, headers)
    return res