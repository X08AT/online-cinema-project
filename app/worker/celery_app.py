import os

from celery import Celery

celery_app = Celery(
    "online_cinema",
    broker=os.getenv("REDIS_URL", "redis://redis:6379"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379"),
)