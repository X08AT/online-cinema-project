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


async def read_notification(
        user_id: int,
        notification_id: int,
        db: AsyncSession
) -> None:
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
    )

    notification = result.scalar_one_or_none()

    if notification is None:
        raise ValueError("Notification not found")

    notification.is_read = True

    await db.commit()
