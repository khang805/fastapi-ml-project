from celery import Celery

# Initialize Celery with Redis as broker and backend
celery_app = Celery(
    "ml_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Configuration for task tracking and result expiration
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600  # Purge results after 1 hour from Redis
)