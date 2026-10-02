from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.certification import (
    delete_certification,
    update_certification,
    create_certification,
)
from app.crud.movie.director import delete_director, update_director, create_director
from app.crud.movie.genre import create_genre, update_genre, delete_genre
from app.crud.movie.movie import delete_movie, update_movie, create_movie
from app.crud.movie.star import update_star, delete_star, create_star
from app.db.dependencies import require_moderator, get_db
from app.models.user import User
from app.schemas.movie.movie import (
    MovieUpdateModel,
    MovieResponseModel,
    MovieCreateModel,
    NamedEntityUpdateModel,
    NamedEntityResponseModel,
    NamedEntityCreateModel,
)

router = APIRouter(tags=["Management"])


@router.post(
    "/genres",
    status_code=201,
    response_model=NamedEntityResponseModel,
    summary="Create genre",
    description=(
        "Creates a new movie genre. " "This operation is available only to moderators."
    ),
)
async def genre_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    genre = await create_genre(data, db)

    return genre


@router.patch(
    "/genres/{genre_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Update genre",
    description=(
        "Updates an existing movie genre by its ID. "
        "This operation is available only to moderators."
    ),
)
async def genre_update(
    data: NamedEntityUpdateModel,
    genre_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    genre = await update_genre(data, genre_id, db)

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.delete(
    "/genres/{genre_id}",
    status_code=200,
    summary="Delete genre",
    description=(
        "Deletes an existing movie genre by its ID. "
        "This operation is available only to moderators."
    ),
)
async def genre_delete(
    genre_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    deleted = await delete_genre(genre_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Genre not found")

    return {"message": "Genre deleted successfully"}


@router.post(
    "/stars",
    status_code=201,
    response_model=NamedEntityResponseModel,
    summary="Create star",
    description=(
        "Creates a new movie star. " "This operation is available only to moderators."
    ),
)
async def star_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    star = await create_star(data, db)

    return star


@router.patch(
    "/stars/{star_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Update star",
    description=(
        "Updates an existing movie star by their ID. "
        "This operation is available only to moderators."
    ),
)
async def star_update(
    data: NamedEntityUpdateModel,
    star_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    star = await update_star(data, star_id, db)

    if star is None:
        raise HTTPException(status_code=404, detail="Star not found")

    return star


@router.delete(
    "/stars/{star_id}",
    status_code=200,
    summary="Delete star",
    description=(
        "Deletes an existing movie star by their ID. "
        "This operation is available only to moderators."
    ),
)
async def star_delete(
    star_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    deleted = await delete_star(star_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Star not found")

    return {"message": "Star deleted successfully"}


@router.post(
    "/directors",
    status_code=201,
    response_model=NamedEntityResponseModel,
    summary="Create director",
    description=(
        "Creates a new movie director. "
        "This operation is available only to moderators."
    ),
)
async def director_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    director = await create_director(data, db)

    return director


@router.patch(
    "/directors/{director_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Update director",
    description=(
        "Updates an existing movie director by their ID. "
        "This operation is available only to moderators."
    ),
)
async def director_update(
    data: NamedEntityUpdateModel,
    director_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    director = await update_director(data, director_id, db)

    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")

    return director


@router.delete(
    "/directors/{director_id}",
    status_code=200,
    summary="Delete director",
    description=(
        "Deletes an existing movie director by their ID. "
        "This operation is available only to moderators."
    ),
)
async def director_delete(
    director_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    deleted = await delete_director(director_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Director not found")

    return {"message": "Director deleted successfully"}


@router.post(
    "/certifications",
    status_code=201,
    response_model=NamedEntityResponseModel,
    summary="Create certification",
    description=(
        "Creates a new movie certification. "
        "This operation is available only to moderators."
    ),
)
async def certification_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    certification = await create_certification(data, db)

    return certification


@router.patch(
    "/certifications/{certification_id}",
    status_code=200,
    response_model=NamedEntityResponseModel,
    summary="Update certification",
    description=(
        "Updates an existing movie certification by its ID. "
        "This operation is available only to moderators."
    ),
)
async def certification_update(
    data: NamedEntityUpdateModel,
    certification_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    certification = await update_certification(data, certification_id, db)

    if certification is None:
        raise HTTPException(status_code=404, detail="Certification not found")

    return certification


@router.delete(
    "/certifications/{certification_id}",
    status_code=200,
    summary="Delete certification",
    description=(
        "Deletes an existing movie certification by its ID. "
        "This operation is available only to moderators."
    ),
)
async def certification_delete(
    certification_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    deleted = await delete_certification(certification_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Certification not found")

    return {"message": "Certification deleted successfully"}


@router.post(
    "/movies",
    status_code=201,
    response_model=MovieResponseModel,
    summary="Create movie",
    description=(
        "Creates a new movie with the provided information. "
        "This operation is available only to moderators."
    ),
)
async def movie_create(
    data: MovieCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    try:
        movie = await create_movie(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return movie


@router.patch(
    "/movies/{movie_id}",
    status_code=200,
    response_model=MovieResponseModel,
    summary="Update movie",
    description=(
        "Updates an existing movie by its ID. "
        "This operation is available only to moderators."
    ),
)
async def movie_update(
    movie_id: int,
    data: MovieUpdateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    try:
        updated_movie = await update_movie(data, movie_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return updated_movie


@router.delete(
    "/movies/{movie_id}",
    status_code=200,
    summary="Delete movie",
    description=(
        "Deletes an existing movie by its ID. "
        "This operation is available only to moderators."
    ),
)
async def movie_delete(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator),
):
    deleted = await delete_movie(movie_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"message": "Movie deleted successfully"}
