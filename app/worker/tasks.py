from app.celery.celery_app import celery_app


@celery_app.task
def test_task():
    return "Celery works!"