from pydantic import BaseModel, Field


class MovieRatingModel(BaseModel):
    rating: int = Field(ge=1, le=10)


class MovieRatingResponseModel(BaseModel):
    average_rating: float | None = None
    ratings_count: int
    user_rating: int | None = None
