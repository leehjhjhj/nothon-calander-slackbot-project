from slack_sdk import WebClient

class Workspace:
    """
    워크스페이스 멤버들 유저 아이디 가져오기
    """
    def __init__(self, token):
        self.client = WebClient(token)

    def get_users(self):
        response = self.client.users_list()
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
