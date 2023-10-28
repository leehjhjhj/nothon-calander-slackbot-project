from .workspace import Workspace
from database import SessionLocal
from api.persistance import NotionSlackMappingRepository
import logging

def make_participants(properties, notion_database_id):
    notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())
    try:
        result = ''
        participants_infos = properties.get("참여자", {}).get("multi_select", [{}])
        participants_names = [participants_info['name'] for participants_info in participants_infos]
        if not participants_names:
            return False
        slack_token = notion_slack_mapping_repo.get_slack_channel_id_by_notion_database_id(notion_database_id)[0]
        workspace = Workspace(token=slack_token)
        name_user_id_map = workspace.get_users()

        for participants_name in participants_names:
            user_id = name_user_id_map.get(f'{participants_name}', False)
            if user_id:
                result += f"<@{user_id}> "
        return result
    
    except Exception as e:
        logging.error(f"참여자 파싱 에러 발생: {e}")
    finally:
        notion_slack_mapping_repo.db.close()