from decouple import config
from slack_sdk import WebClient

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
            blocks = [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }]
        )
        return result

slack_token = config('SLACK_API_TOKEN')
channel_id = config('SLACK_CHANNEL_ID')

def schedule_one_day_before(**kwargs):
    slack = SendToSlackAPI(slack_token, channel_id)

    time = "1시"
    name = "회의"
    meeting_url = "www.naver.com"

    message = f"{time}에 {name} 회의가 예정되어있어요! 잊지 마세요.😂 \n 회의 노션페이지: {meeting_url}"
    slack.send_message(message)

schedule_one_day_before()