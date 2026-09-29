from typing import Literal

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.favorite import (
    remove_movie_from_favorite,
    favorite_movies_list,
    favorite_movie_by_id
)
from app.db.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.movie.favorite import FavoriteResponseModel
from app.schemas.movie.movie import MovieResponseModel

router = APIRouter(tags=["Favorites"])


@router.get(
    "/movies/favorites",
    status_code=200,
    response_model=list[MovieResponseModel],
    summary="Get favorite movies",
    description=(
        "Returns the authenticated user's favorite movies. "
        "Supports pagination, filtering, sorting, and searching."
    ),
)
async def get_favorites(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        year: int | None = Query(default=None, ge=1888),
        imdb: float | None = Query(default=None, ge=0, le=10),
        sort_by: Literal["price", "year", "votes"] | None = Query(
            default=None
        ),
        sort_order: Literal["asc", "desc"] = Query(default="asc"),
        search: str | None = Query(default=None),
):
    movies = await favorite_movies_list(
        current_user.id,
        db,
        skip,
        limit,
        year,
        imdb,
        sort_by,
        sort_order,
        search
    )

    return movies


@router.post(
    "/movies/{movie_id}/favorite",
    status_code=201,
    response_model=FavoriteResponseModel,
    summary="Add movie to favorites",
    description=(
        "Adds the specified movie to the authenticated user's favorites."
    ),
)
async def favorite_movie(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        favorite = await favorite_movie_by_id(current_user.id, movie_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return favorite


@router.delete(
    "/movies/{movie_id}/favorite",
    status_code=204,
    summary="Remove movie from favorites",
    description=(
        "Removes the specified movie from the authenticated user's favorites."
    ),
)
async def delete_favorite(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await remove_movie_from_favorite(movie_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
