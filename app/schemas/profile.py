from datetime import date

from fastapi import Form
from pydantic import BaseModel, ConfigDict

from app.models.user import GenderEnum


class ProfileCreateModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None
    info: str

    @classmethod
    def as_form(
            cls,
            first_name: str | None = Form(None),
            last_name: str | None = Form(None),
            gender: GenderEnum | None = Form(None),
            date_of_birth: date | None = Form(None),
            info: str = Form(...),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
        )


class ProfileCreateResponseModel(BaseModel):
    id: int
    user_id: int
    first_name: str | None
    last_name: str | None
    gender: GenderEnum | None
    avatar: str | None
    date_of_birth: date | None
    info: str

    model_config = ConfigDict(from_attributes=True)
