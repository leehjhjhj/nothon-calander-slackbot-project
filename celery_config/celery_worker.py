from celery import shared_task
from decouple import config
from .send_message import SendToSlackAPI

slack_token = config('SLACK_API_TOKEN')
channel_id = config('SLACK_CHANNEL_ID')

@shared_task
def schedule_one_day_before(**kwargs):
    slack = SendToSlackAPI(slack_token, channel_id)

    time = kwargs.get('time')
    name = kwargs.get('name')
    meeting_url = kwargs.get('meeting_url')

    message = f"{time}에 {name} 회의가 예정되어있어요! 잊지 마세요.\n 회의 노션페이지: {meeting_url}"
    slack.send_message(message)

@shared_task
def schedule_ten_minutes_before(**kwargs):
    slack = SendToSlackAPI(slack_token, channel_id)

    name = kwargs.get('name')
    meeting_url = kwargs.get('meeting_url')

    message = f"곧 10분 뒤에 {name} 회의가 시작돼요! 모두 준비해주세요.\n 회의 노션페이지: {meeting_url}"
    slack.send_message(message)