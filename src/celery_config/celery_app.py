from celery import Celery
from decouple import config

redis_host = config('REDIS_HOST')
redis_port = config('REDIS_PORT')

celery_task = Celery(
    'app',
    broker=f"redis://{redis_host}:{redis_port}/0",
    backend=f"redis://{redis_host}:{redis_port}/1",
    include=['celery_config.celery_beat', 'celery_config.celery_worker']
)

celery_task.conf.update(
    timezone='Asia/Seoul',
)

celery_task.conf.broker_transport_options = {'visibility_timeout': 31536000} 