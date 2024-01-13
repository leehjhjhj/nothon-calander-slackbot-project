from .celery_app import celery_task
from datetime import timedelta 
from .containers import MeetingContainer
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
    meeting_process = MeetingContainer.meeting_process()
    meeting_process.save_meeting()
