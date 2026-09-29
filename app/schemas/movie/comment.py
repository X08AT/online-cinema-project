from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict


class CommentCreateModel(BaseModel):
    content: str = Field(min_length=4)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 4:
            raise ValueError("Comment must contain at least 4 characters")

        return value


class CommentUpdateModel(CommentCreateModel):
    pass


class CommentResponseModel(BaseModel):
    id: int
    user_id: int
    movie_id: int
    parent_id: int | None = None
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int
    replies: list["ReplyResponseModel"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ReplyResponseModel(BaseModel):
    id: int
    user_id: int
    movie_id: int
    parent_id: int | None
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int

    model_config = ConfigDict(from_attributes=True)
