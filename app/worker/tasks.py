import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.settings import settings
from app.models.user import ActivationToken
from app.worker.celery_app import celery_app


@celery_app.task
def test_task():
    return "Celery works!"


async def async_cleanup_expired_activation_tokens():

    engine = create_async_engine(settings.DATABASE_URL)

    SessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with SessionLocal() as db:

        result = await db.execute(
            select(ActivationToken).where(
                ActivationToken.expires_at < datetime.now(timezone.utc)
            )
        )

        expired_tokens = result.scalars().all()

        for expired_token in expired_tokens:
            await db.delete(expired_token)

        await db.commit()

    await engine.dispose()


@celery_app.task
def cleanup_expired_activation_tokens():
    asyncio.run(async_cleanup_expired_activation_tokens())
