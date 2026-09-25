from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class NamedEntityResponseModel(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NamedEntityCreateModel(BaseModel):
    name: str


class NamedEntityUpdateModel(NamedEntityCreateModel):
    pass


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

    model_config = ConfigDict(from_attributes=True)
