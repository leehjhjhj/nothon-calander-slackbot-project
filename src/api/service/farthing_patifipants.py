from utils.redis_connect import get_redis_connection
from database import SessionLocal
from api.persistance import SlackRepository
import logging
import json

def make_participants(result, notion_database_id):
    slack_repo = SlackRepository(db=SessionLocal())
    try:
        mention = ''
        participants_infos = result.get('properties', {}).get("참여자", {}).get("multi_select", [{}])
        participants_names = [participants_info['name'] for participants_info in participants_infos]
        if not participants_names:
            return False
        
        slack_channel_id = slack_repo.get_slack_channel_id_by_notion_database_id(notion_database_id)
        redis_conn = get_redis_connection(db_select=3)
        name_user_id_map_byte = redis_conn.get(f"{slack_channel_id}")
        name_user_id_map = json.loads(name_user_id_map_byte)

        for participants_name in participants_names:
            user_id = name_user_id_map.get(f'{participants_name}', False)
            if user_id:
                mention += f"<@{user_id}> "
        return mention
    
    except Exception as e:
        logging.error(f"참여자 파싱 에러 발생: {e}")
    finally:
        slack_repo.db.close()