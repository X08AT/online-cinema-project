from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.certification import (
    get_certification_by_id,
    get_certifications
)
from app.crud.movie.director import get_directors, get_director_by_id
from app.crud.movie.genre import get_genres, get_genre_by_id
from app.crud.movie.movie import (
    get_movies_by_genre,
    get_movies,
    get_movie_by_id
)
from app.crud.movie.star import get_stars, get_star_by_id
from app.db.dependencies import get_db
from app.schemas.movie.movie import (
    GenreWithCountResponseModel,
    NamedEntityResponseModel,
    MovieResponseModel
)

router = APIRouter(tags=["Catalog"])


@router.get(
    "/genres",
    status_code=200,
    response_model=list[GenreWithCountResponseModel],
    summary="Get genres",
    description=(
        "Returns a list of all available movie genres "
        "with the number of movies in each genre."
    ),
)
async def genres_list(db: AsyncSession = Depends(get_db)):
    genres = await get_genres(db)

    return genres


@router.get(
    "/genres/{genre_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Get genre by ID",
    description=(
        "Returns a specific movie genre by its ID."
    ),
)
async def genre_get_by_id(genre_id: int, db: AsyncSession = Depends(get_db)):
    genre = await get_genre_by_id(genre_id, db)

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.get(
    "/stars",
    status_code=200,
    response_model=list[NamedEntityResponseModel],
    summary="Get stars",
    description=(
        "Returns a list of all available movie stars."
    ),
)
async def stars_list(
    db: AsyncSession = Depends(get_db)
):
    stars = await get_stars(db)

    return stars


@router.get(
    "/stars/{star_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Get star by ID",
    description=(
        "Returns a specific movie star by their ID."
    ),
)
async def star_get_by_id(
    star_id: int,
    db: AsyncSession = Depends(get_db)
):
    star = await get_star_by_id(star_id, db)

    if star is None:
        raise HTTPException(
            status_code=404,
            detail="Star not found"
        )

    return star


@router.get(
    "/directors",
    status_code=200,
    response_model=list[NamedEntityResponseModel],
    summary="Get directors",
    description=(
        "Returns a list of all available movie directors."
    ),
)
async def directors_list(
    db: AsyncSession = Depends(get_db)
):
    directors = await get_directors(db)

    return directors


@router.get(
    "/directors/{director_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Get director by ID",
    description=(
        "Returns a specific movie director by their ID."
    ),
)
async def director_get_by_id(
    director_id: int,
    db: AsyncSession = Depends(get_db)
):
    director = await get_director_by_id(director_id, db)

    if director is None:
        raise HTTPException(
            status_code=404,
            detail="Director not found"
        )

    return director


@router.get(
    "/certifications",
    status_code=200,
    response_model=list[NamedEntityResponseModel],
    summary="Get certifications",
    description=(
        "Returns a list of all available movie certifications."
    ),
)
async def certifications_list(
    db: AsyncSession = Depends(get_db)
):
    certifications = await get_certifications(db)

    return certifications


@router.get(
    "/certifications/{certification_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Get certification by ID",
    description=(
        "Returns a specific movie certification by its ID."
    ),
)
async def certification_get_by_id(
    certification_id: int,
    db: AsyncSession = Depends(get_db)
):
    certification = await get_certification_by_id(
        certification_id,
        db
    )

    if certification is None:
        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    return certification


@router.get(
    "/movies",
    status_code=200,
    response_model=list[MovieResponseModel],
    summary="Get movies",
    description=(
        "Returns a paginated list of movies. Supports filtering by year "
        "and IMDb rating, sorting by price, year, or popularity, and "
        "searching by movie-related information."
    ),
)
async def movies_list(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    year: int | None = Query(default=None, ge=1888),
    imdb: float | None = Query(default=None, ge=0, le=10),
    sort_by: Literal["price", "year", "votes"] | None = Query(default=None),
    sort_order: Literal["asc", "desc"] = Query(default="asc"),
    search: str | None = Query(default=None),
):
    movies = await get_movies(
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


@router.get(
    "/movies/{movie_id}",
    status_code=200,
    response_model=MovieResponseModel,
    summary="Get movie by ID",
    description=(
        "Returns detailed information about a specific movie by its ID."
    ),
)
async def movie_get_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@router.get(
    "/genres/{genre_id}/movies",
    status_code=200,
    response_model=list[MovieResponseModel],
    summary="Get movies by genre",
    description=(
        "Returns a list of movies associated with the specified genre."
    ),
)
async def movie_list_by_genre(
        genre_id: int,
        db: AsyncSession = Depends(get_db)
):
    movies = await get_movies_by_genre(genre_id, db)

    return movies
