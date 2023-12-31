from slack_sdk import WebClient
from datetime import datetime

class SendToSlackAPI:
    """
    slack 메시지 API
    """
    def __init__(self, token, channel_id):
        self.client = WebClient(token)
        self.channel_id = channel_id

    def send_message(self, message):
        result = self.client.chat_postMessage(
            channel = self.channel_id,
            blocks = [

                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "divider"
                },
            ]
        )
        return result
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
        
slack_token = ''
channel_id = "C05TJF8B21F"
slack = SendToSlackAPI(slack_token, channel_id)

def transform_date(time):
    am_pm = "오후" if time.hour >= 12 else "오전"
    hour_12 = time.hour - 12 if time.hour > 12 else time.hour
    formatted_time = f"{time.month}월 {time.day}일 {am_pm} {hour_12}시 {time.minute}분"
    return formatted_time

def schedule_one_day_before():
    time = datetime.now()
    name = "긴급회의 1일차"
    meeting_url = "test.com"
    meeting_type = "긴급회의"
    participants = "@이현제, @이현제"
    transformed_date = transform_date(time)
    message = f">:bell: {transformed_date}에 \"{name}\" 회의가 예정되어있어요! 잊지 마세요. :joy:\n" \
            f"> 회의 타입: `{meeting_type}`\n" \
            f"> 회의 노션페이지: <{meeting_url}|바로가기>"
    
    message = f">:bangbang: 곧 10분 뒤에 \"{name}\" 가 시작돼요! 모두 준비해주세요.\n" \
            f"> 회의 노션페이지: <{meeting_url}|바로가기>\n" \
    f"> 참여자:<@U05SX0GLNR1>"

    slack.send_message(message)

def get_users_id():
    print(slack.get_users())
#schedule_one_day_before()
get_users_id()