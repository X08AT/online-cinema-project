from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteResponseModel(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
