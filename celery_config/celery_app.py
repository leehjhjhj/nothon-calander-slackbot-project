from celery import Celery

celery_task = Celery(
    'app',
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=['celery_config.celery_beat', 'celery_config.celery_worker']
)

