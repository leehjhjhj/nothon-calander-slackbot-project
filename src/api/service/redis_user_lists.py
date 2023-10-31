from utils.redis_connect import get_redis_connection
from decouple import config
from .workspace import Workspace
from api.persistance import SlackRepository
from api.persistance import NotionSlackMappingRepository
from database import SessionLocal
import logging
import json

def save_user_lists_to_redis():
    slack_repo = SlackRepository(db=SessionLocal())
    notion_slack_repo = NotionSlackMappingRepository(db=SessionLocal())
    redis_con = get_redis_connection(db_select=3)
    try:
        slack_ids = notion_slack_repo.get_all_slack_channels()
        for slack_id in slack_ids:
            slack_token = slack_repo.get_api_token_by_slack_channel_id(slack_id)
            workspace = Workspace(slack_token)
            name_user_id_map = workspace.get_users()
            name_user_id_bytes = json.dumps(name_user_id_map)
            redis_con.set(f"{slack_id}", name_user_id_bytes)
    except Exception as e:
        logging.error(f"레디스 유저리스트 저장 오류 발생: {e}")
    finally:
        slack_repo.db.close()
        notion_slack_repo.db.close()