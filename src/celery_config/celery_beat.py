from .celery_app import celery_task
from datetime import timedelta 
from api.service.save_meeting_facade import save_meeting_facade
from decouple import config

SCHEDULE_TIME_UNITS = config('SCHEDULE_TIME_UNITS')
SCHEDULE_PARAMETER = config('SCHEDULE_PARAMETER')
print(SCHEDULE_TIME_UNITS, SCHEDULE_PARAMETER)

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beat.schedule_meeting',
        'schedule': timedelta(**{SCHEDULE_TIME_UNITS: int(SCHEDULE_PARAMETER)})
    },
}

@celery_task.task
def schedule_meeting():
    save_meeting_facade()
