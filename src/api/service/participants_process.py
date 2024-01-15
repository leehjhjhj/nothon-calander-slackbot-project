import logging
from entity import NotionPage
from slack_sdk import WebClient
from utils.redis_connect import get_cache_redis_connection
import json

class ParticipantsProcess:
    def __init__(self, slack_repository, notion_slack_mapping_repository):
        self._slack_repo = slack_repository
        self._notion_slack_mapping_repo = notion_slack_mapping_repository
        self._redis_conn = get_cache_redis_connection(db_select=3)

    def add_participants(self, meeting: NotionPage, result) -> NotionPage:
        participants = self._make_participants(result, meeting.notion_database_id)
        meeting.participants = participants if participants else None
        return meeting
            
    def save_user_lists_to_redis(self):
        slack_ids = self._notion_slack_mapping_repo.get_all_slack_channels()
        for slack_id in slack_ids:
            try:
                slack_token = self._slack_repo.get_api_token_by_slack_channel_id(slack_id)
                name_user_id_map = self._get_slack_users(slack_token)
                name_user_id_bytes = json.dumps(name_user_id_map)
                self._redis_conn.set(f"{slack_id}", name_user_id_bytes)
            except Exception as e:
                logging.error(f"레디스 유저리스트 저장 오류 발생: {e}")

    def _make_participants(self, result, notion_database_id):
        try:
            mention = ''
            participants_infos = result.get('properties', {}).get("참여자", {}).get("multi_select", [{}])
            participants_names = [participants_info['name'] for participants_info in participants_infos]
            if not participants_names:
                return False

            slack_channel_id = self._slack_repo.get_slack_channel_id_by_notion_database_id(notion_database_id)
            name_user_id_map_byte = self._redis_conn.get(f"{slack_channel_id}")
            name_user_id_map = json.loads(name_user_id_map_byte)

            for participants_name in participants_names:
                print(name_user_id_map, participants_names, slack_channel_id, self._redis_conn)
                user_id = name_user_id_map.get(f'{participants_name}', False)
                if user_id:
                    mention += f"<@{user_id}> "
            return mention
        
        except Exception as e:
            logging.error(f"참여자 파싱 에러 발생: {e}")

    def _get_slack_users(self, slack_token):
        client = WebClient(slack_token)
        response = client.users_list()
        if response['ok']:
            members = response['members']
            name_id_map = {}
            for member in members:
                id = member.get('id')
                name = member.get('real_name')
                name_id_map[f'{name}'] = id
            return name_id_map
        else:
            return None
