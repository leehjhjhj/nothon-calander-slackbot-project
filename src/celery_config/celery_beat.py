from .celery_app import celery_task
from datetime import timedelta 
from api.service.save_meeting_facade import save_meeting_facade

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beat.schedule_meeting',
        'schedule': timedelta(hours=1)
    },
}

@celery_task.task
def schedule_meeting():
    save_meeting_facade()
