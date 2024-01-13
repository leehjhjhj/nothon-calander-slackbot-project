from .celery_app import celery_task
from datetime import timedelta 
from .containers import MeetingContainer

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beat.schedule_meeting',
        'schedule': timedelta(seconds=15)
    },
}

@celery_task.task
def schedule_meeting():
    meeting_process = MeetingContainer.meeting_process()
    meeting_process.save_meeting()
