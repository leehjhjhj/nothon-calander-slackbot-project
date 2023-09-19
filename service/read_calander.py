import requests
from decouple import config

def read_database():
    token = config('NOTION_TOKEN')
    database_id = config('NOTION_DATABASE_ID')
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }
    readUrl = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    return data
