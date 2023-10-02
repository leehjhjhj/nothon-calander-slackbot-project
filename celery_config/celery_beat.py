from .celery_app import celery_task
from service.save_meeting_facade import save_meeting_facade
from datetime import timedelta 

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beat.read_calander_schedule',
        'schedule': timedelta(minutes=20)
    },
}

def read_calander_schedule():
    save_meeting_facade()
