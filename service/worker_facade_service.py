from celery_config.celery_worker import schedule_one_day_before, schedule_ten_minutes_before
from datetime import timedelta

def worker_facade(meeting):
    extra = {
        "page_id" : meeting.page_id,
        "time": meeting.time,
        "meeting_url" : meeting.meeting_url,
        "name" : meeting.name,
        "meeting_type": meeting.meeting_type,
    }
    reminder_time_one_day = meeting.time - timedelta(days=1)
    reminder_time_ten_minutes = meeting.time - timedelta(minutes=10)

    schedule_one_day_before.apply_async(kwargs=extra, eta=reminder_time_one_day)
    schedule_ten_minutes_before.apply_async(kwargs=extra, eta=reminder_time_ten_minutes)
    