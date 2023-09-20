from .celery_app import celery_task
from datetime import timedelta
from service.save_meeting_facade import save_meeting_facade

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beatr.kk',
        'schedule': timedelta(seconds=1),
    },
}

@celery_task.task
def read_calander_schedule():
    save_meeting_facade()
