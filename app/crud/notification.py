from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Notification


async def get_notifications(
        user_id: int,
        db: AsyncSession
) -> list[Notification]:
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()
