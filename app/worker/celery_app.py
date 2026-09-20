from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings


celery_app = Celery(
    "online_cinema",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.worker.tasks"],
)

celery_app.conf.beat_schedule = {
    "cleanup_expired_activation_tokens": {
        "task": "app.worker.tasks.cleanup_expired_activation_tokens",
        "schedule": crontab(hour=0, minute=0),
    }
}
