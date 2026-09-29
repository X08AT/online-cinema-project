from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.notification import get_notifications, read_notification
from app.db.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.movie.notification import NotificationResponseModel

router = APIRouter()


@router.get(
    "/notifications",
    status_code=200,
    response_model=list[NotificationResponseModel]
)
async def notifications_list(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    notifications = await get_notifications(current_user.id, db)

    return notifications


@router.patch("/notifications/{notification_id}", status_code=200)
async def notification_read(
        notification_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await read_notification(current_user.id, notification_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Notification read successfully"}
