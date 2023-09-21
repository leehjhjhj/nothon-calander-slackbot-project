from celery import shared_task
from decouple import config
from .send_message import SendToSlackAPI
from .check_cancel import check_status

slack_token = config('SLACK_API_TOKEN')
channel_id = config('SLACK_CHANNEL_ID')

def transform_date(time):
    am_pm = "오후" if time.hour >= 12 else "오전"
    hour_12 = time.hour - 12 if time.hour > 12 else time.hour
    formatted_time = f"{time.month}월 {time.day}일 {am_pm} {hour_12}시 {time.minute}분"
    return formatted_time

@shared_task
def schedule_one_day_before(**kwargs):
    slack = SendToSlackAPI(slack_token, channel_id)

    page_id = kwargs.get('page_id')
    time = kwargs.get('time')
    name = kwargs.get('name')
    meeting_url = kwargs.get('meeting_url')
    meeting_type = kwargs.get('meeting_type')
    
    transformed_date = transform_date(time)
    message = f">:bell: *{transformed_date}에 \"{name}\"* 회의가 예정되어있어요! 잊지 마세요. :joy:\n" \
          f"> 회의 타입: `{meeting_type}`\n" \
          f"> 회의 노션페이지: <{meeting_url}|바로가기>"
    
    if check_status(page_id):
        slack.send_message(message)

@shared_task
def schedule_ten_minutes_before(**kwargs):
    slack = SendToSlackAPI(slack_token, channel_id)
    
    page_id = kwargs.get('page_id')
    name = kwargs.get('name')
    meeting_url = kwargs.get('meeting_url')

    message = f">:bangbang: 곧 10분 뒤에 *\"{name}\"* 가 시작돼요! 모두 준비해주세요. :laughing:\n> 회의 노션페이지: <{meeting_url}|바로가기>"

    if check_status(page_id):
        slack.send_message(message)