from .celery_app import celery_task
from datetime import timedelta 
from api.service.containers import MeetingContainer
from decouple import config

SCHEDULE_TIME_UNITS = config('SCHEDULE_TIME_UNITS')
SCHEDULE_PARAMETER = config('SCHEDULE_PARAMETER')

celery_task.conf.beat_schedule = {
    'schedule-meetings-every-hour': {
        'task': 'celery_config.celery_beat.schedule_meeting',
        'schedule': timedelta(**{SCHEDULE_TIME_UNITS: int(SCHEDULE_PARAMETER)})
    },
    'schedule-redis_user_list-every-day': {
        'task': 'celery_config.celery_beat.schedule_redis_user_list',
        'schedule': timedelta(days=1)
    },
}

@celery_task.task
def schedule_meeting():
    meeting_process = MeetingContainer.meeting_process()
    meeting_process.save_meeting()

@celery_task.task
def schedule_redis_user_list():
    participants_process = MeetingContainer.participants_process()
    participants_process.save_user_lists_to_redis()