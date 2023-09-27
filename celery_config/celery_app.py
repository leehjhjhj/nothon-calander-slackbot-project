from celery import Celery
from decouple import config

redis_host = config('REDIS_HOST')

celery_task = Celery(
    'app',
    broker=f"redis://{redis_host}:6379/0",
    backend=f"redis://{redis_host}:6379/1",
    include=['celery_config.celery_beat', 'celery_config.celery_worker']
)

celery_task.conf.update(
    timezone='Asia/Seoul',
)
