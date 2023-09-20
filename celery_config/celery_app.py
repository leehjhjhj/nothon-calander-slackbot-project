from celery import Celery

celery_task = Celery(
    'app',
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/1",
    include=['celery_config.celery_beat', 'celery_config.celery_worker']
)

