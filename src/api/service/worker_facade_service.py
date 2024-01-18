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
        schedule_periods = [
            {"period": "one_day", "delta": timedelta(days=1), "task": schedule_one_day_before},
            {"period": "five_hours", "delta": timedelta(hours=5), "task": schedule_five_hours_before},
            {"period": "ten_minutes", "delta": timedelta(minutes=10), "task": schedule_ten_minutes_before},
        ]

        for schedule in schedule_periods:
            reminder_time = meeting.time - schedule["delta"]
            uuid = make_uuid(meeting.page_id, schedule["period"])
            res = AsyncResult(id=uuid, app=celery_task)

            if not res.ready():
                schedule["task"].apply_async(kwargs=extra, eta=reminder_time, task_id=uuid)

    except Exception as e:
        logging.error('Error in worker_facade', exc_info=e)
    