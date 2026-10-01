from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.rating import (
    set_movie_rating,
    delete_movie_rating,
    get_movie_ratings,
)
from app.db.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.movie.rating import MovieRatingModel, MovieRatingResponseModel

router = APIRouter(tags=["Ratings"])


@router.patch(
    "/movies/{movie_id}/rating",
    status_code=200,
    summary="Rate movie",
    description=(
        "Sets or updates the authenticated user's rating for the " "specified movie."
    ),
)
async def rate_movie(
    movie_id: int,
    data: MovieRatingModel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await set_movie_rating(movie_id, current_user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Movie rated successfully"}


@router.delete(
    "/movies/{movie_id}/rating",
    status_code=204,
    summary="Delete movie rating",
    description=("Deletes the authenticated user's rating for the specified movie."),
)
async def delete_rating(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_movie_rating(movie_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/movies/{movie_id}/ratings",
    status_code=200,
    response_model=MovieRatingResponseModel,
    summary="Get movie ratings",
    description=(
        "Returns rating information for the specified movie, including "
        "rating data related to the authenticated user."
    ),
)
async def get_ratings(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        movie_ratings = await get_movie_ratings(movie_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return movie_ratings
