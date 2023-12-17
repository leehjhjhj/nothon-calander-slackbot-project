from celery_config.celery_worker import schedule_one_day_before, schedule_five_hours_before, schedule_ten_minutes_before
from datetime import timedelta
from celery.result import AsyncResult
from celery_config.celery_app import celery_task
import logging
from entity import NotionPage

def make_uuid(page_id, cmd):
    head = ''
    if cmd == "one_day":
        head = "1-day-"
    elif cmd == "ten_min":
        head = "10-min-"
    return head + page_id

def worker_facade(meeting: NotionPage):
    logging.info('in worker facade')
    try:
        extra = {
            "page_id" : meeting.page_id,
            "time": meeting.time,
            "meeting_url" : meeting.meeting_url,
            "name" : meeting.name,
            "meeting_type": meeting.meeting_type,
            "notion_database_id": meeting.notion_database_id,
            "participants": meeting.participants,
        }
        reminder_time_one_day = meeting.time - timedelta(days=1)
        one_day_uuid = make_uuid(meeting.page_id, "one_day")
        res_one_day = AsyncResult(id=one_day_uuid, app=celery_task)

        reminder_time_five_hours = meeting.time - timedelta(hours=5)
        five_hours_uuid = make_uuid(meeting.page_id, "five_hours")
        res_five_hours = AsyncResult(id=one_day_uuid, app=celery_task)

        reminder_time_ten_minutes = meeting.time - timedelta(minutes=10)
        ten_min_uuid = make_uuid(meeting.page_id, "ten_min")
        res_ten_min = AsyncResult(id=ten_min_uuid, app=celery_task)
        
        if not res_one_day.ready():
            schedule_one_day_before.apply_async(kwargs=extra, eta=reminder_time_one_day, task_id=one_day_uuid)
        
        if not res_five_hours.ready():
            schedule_five_hours_before.apply_async(kwargs=extra, eta=reminder_time_five_hours, task_id=five_hours_uuid)

        if not res_ten_min.ready():
            schedule_ten_minutes_before.apply_async(kwargs=extra, eta=reminder_time_ten_minutes, task_id=ten_min_uuid)

    except Exception as e:
        logging.error(f"에러 발생: {e}")
    