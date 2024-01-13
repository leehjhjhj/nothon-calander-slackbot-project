import logging
from entity import NotionPage
from slack_sdk import WebClient

class ParticipantsProcess:
    def __init__(self, slack_repository):
        self._slack_repo = slack_repository

    def add_participants(self, meeting: NotionPage, result) -> NotionPage:
        participants = self._make_participants(result, meeting.notion_database_id)
        meeting.participants = participants if participants else None
        return meeting
    
    def _make_participants(self, result, notion_database_id):
        try:
            mention = ''
            participants_infos = result.get('properties', {}).get("참여자", {}).get("multi_select", [{}])
            participants_names = [participants_info['name'] for participants_info in participants_infos]
            if not participants_names:
                return False
            slack_token = self._slack_repo.get_api_token_by_notion_database_id(notion_database_id)
            logging.info('users.list api 호출')
            name_user_id_map = self._get_slack_users(slack_token)

            for participants_name in participants_names:
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