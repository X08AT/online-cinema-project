from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator


class NamedEntityResponseModel(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NamedEntityCreateModel(BaseModel):
    name: str


class NamedEntityUpdateModel(NamedEntityCreateModel):
    pass


class GenreWithCountResponseModel(NamedEntityResponseModel):
    movie_count: int


class MovieCreateModel(BaseModel):
    name: str = Field(min_length=1)
    year: int = Field(ge=1888)
    time: int = Field(gt=0)
    imdb: float = Field(ge=0, le=10)
    votes: int = Field(ge=0)
    meta_score: float | None = Field(default=None, ge=0, le=100)
    gross: float | None = Field(default=None, ge=0)
    description: str = Field(min_length=1)
    price: Decimal = Field(gt=0)
    certification_id: int = Field(gt=0)
    genre_ids: set[int]
    star_ids: set[int]
    director_ids: set[int]


class MovieUpdateModel(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=1888)
    time: int | None = Field(default=None, gt=0)
    imdb: float | None = Field(default=None, ge=0, le=10)
    votes: int | None = Field(default=None, ge=0)
    meta_score: float | None = Field(default=None, ge=0, le=100)
    gross: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(default=None, gt=0)
    certification_id: int | None = Field(default=None, gt=0)
    genre_ids: set[int] | None = None
    star_ids: set[int] | None = None
    director_ids: set[int] | None = None


class MovieResponseModel(BaseModel):
    id: int
    uuid: UUID
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: float | None
    gross: float | None
    description: str
    price: Decimal
    certification: NamedEntityResponseModel
    genres: list[NamedEntityResponseModel]
    stars: list[NamedEntityResponseModel]
    directors: list[NamedEntityResponseModel]
    likes_count: int
    dislikes_count: int

    model_config = ConfigDict(from_attributes=True)


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


class MovieRatingModel(BaseModel):
    rating: int = Field(ge=1, le=10)
