import requests

def read_notion_database(notion_database_id, notion_api_key):
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
