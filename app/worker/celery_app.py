from celery import Celery

from app.core.settings import settings


celery_app = Celery(
    "online_cinema",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)
