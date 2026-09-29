from pydantic import BaseModel

from app.models.user import UserGroupEnum


class AdminChangeGroupModel(BaseModel):
    user_group: UserGroupEnum
