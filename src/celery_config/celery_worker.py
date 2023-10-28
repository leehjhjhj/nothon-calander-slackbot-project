from .send_message import SendToSlackAPI
from .check_cancel import check_status
from api.persistance.notion_slack_mapping_repository import NotionSlackMappingRepository
from api.persistance.slack_repository import SlackRepository
from database import SessionLocal
from celery_config.celery_app import celery_task

def transform_date(time):
    am_pm = "오후" if time.hour >= 12 else "오전"
    hour_12 = time.hour - 12 if time.hour > 12 else time.hour
    formatted_time = f"{time.month}월 {time.day}일 {am_pm} {hour_12}시 {time.minute}분"
    return formatted_time

@celery_task.task
def schedule_one_day_before(**kwargs):
    notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())
    slack_repo = SlackRepository(db=SessionLocal())
    try:
        page_id = kwargs.get('page_id')
        time = kwargs.get('time')
        name = kwargs.get('name')
        meeting_url = kwargs.get('meeting_url')
        meeting_type = kwargs.get('meeting_type')
        participants = kwargs.get('participants')
        
        notion_database_id = kwargs.get('notion_database_id')
        slack_channel_ids = notion_slack_mapping_repo.get_slack_channel_id_by_notion_database_id(notion_database_id)

        transformed_date = transform_date(time)
        message = f">:bell: {transformed_date}에 \"{name}\" 회의가 예정되어있어요! 잊지 마세요. \n" \
            f"> 회의 타입: `{meeting_type}`\n" \
            f"> 회의 노션페이지: <{meeting_url}|바로가기>\n"\
            f"> 참여자: {participants}"
        
        if check_status(page_id):
            for slack_channel_id in slack_channel_ids:
                slack_token = slack_repo.get_api_token_by_slack_channel_id(slack_channel_id)
                slack = SendToSlackAPI(slack_token, slack_channel_id) 
                slack.send_message(message)
                print(f"{message} 전송 완료")

    except Exception as e:
        print(f"전송실패: {e}")
    finally:
        notion_slack_mapping_repo.db.close()
        slack_repo.db.close()

@celery_task.task
def schedule_ten_minutes_before(**kwargs):
    notion_slack_mapping_repo = NotionSlackMappingRepository(db=SessionLocal())
    slack_repo = SlackRepository(db=SessionLocal())

    try:
        page_id = kwargs.get('page_id')
        name = kwargs.get('name')
        meeting_url = kwargs.get('meeting_url')
        participants = kwargs.get('participants')

        notion_database_id = kwargs.get('notion_database_id')
        slack_channel_ids = notion_slack_mapping_repo.get_slack_channel_id_by_notion_database_id(notion_database_id)

        message = f">:bangbang: 곧 10분 뒤에 \"{name}\" 가 시작돼요! 모두 준비해주세요.\n" \
            f"> 회의 노션페이지: <{meeting_url}|바로가기>\n" \
            f"> 참여자: {participants}"

        if check_status(page_id):
            for slack_channel_id in slack_channel_ids:
                slack_token = slack_repo.get_api_token_by_slack_channel_id(slack_channel_id)
                slack = SendToSlackAPI(slack_token, slack_channel_id)
                slack.send_message(message)
                print(f"{message} 전송 완료")

    except Exception as e:
        print(f"전송실패: {e}")
    finally:
        notion_slack_mapping_repo.db.close()
        slack_repo.db.close()
