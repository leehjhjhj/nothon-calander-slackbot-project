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