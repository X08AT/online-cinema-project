from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.movie import NotificationTypeEnum


class NotificationResponseModel(BaseModel):
    id: int
    user_id: int
    comment_id: int
    notification_type: NotificationTypeEnum
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
