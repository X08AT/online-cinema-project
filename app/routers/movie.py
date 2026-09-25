from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.certification import (
    create_certification,
    get_certifications,
    get_certification_by_id,
    update_certification,
    delete_certification
)
from app.crud.director import (
    create_director,
    get_directors,
    get_director_by_id,
    update_director,
    delete_director
)
from app.crud.genre import (
    create_genre,
    get_genres,
    get_genre_by_id,
    update_genre,
    delete_genre
)
from app.crud.movie import create_movie, get_movies
from app.crud.star import (
    create_star,
    get_stars,
    get_star_by_id,
    update_star,
    delete_star
)
from app.db.dependencies import get_db, require_moderator
from app.models.user import User
from app.schemas.movie import (
    NamedEntityUpdateModel,
    NamedEntityResponseModel,
    NamedEntityCreateModel,
    MovieResponseModel,
    MovieCreateModel
)

router = APIRouter()


@router.post(
    "/genres",
    status_code=201,
    response_model=NamedEntityResponseModel
)
async def genre_create(
        data: NamedEntityCreateModel,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
):
    genre = await create_genre(data, db)

    return genre


@router.get(
    "/genres",
    status_code=200,
    response_model=list[NamedEntityResponseModel]
)
async def genres_list(db: AsyncSession = Depends(get_db)):
    genres = await get_genres(db)

    return genres


@router.get(
    "/genres/{genre_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
)
async def genre_get_by_id(genre_id: int, db: AsyncSession = Depends(get_db)):
    genre = await get_genre_by_id(genre_id, db)

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.patch(
    "/genres/{genre_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
)
async def genre_update(
        data: NamedEntityUpdateModel,
        genre_id: int,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
):
    genre = await update_genre(data, genre_id, db)

    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.delete("/genres/{genre_id}", status_code=200)
async def genre_delete(
        genre_id: int,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
):
    deleted = await delete_genre(genre_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Genre not found")

    return {"message": "Genre deleted successfully"}


@router.post(
    "/stars",
    status_code=201,
    response_model=NamedEntityResponseModel
)
async def star_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    star = await create_star(data, db)

    return star


@router.get(
    "/stars",
    status_code=200,
    response_model=list[NamedEntityResponseModel]
)
async def stars_list(
    db: AsyncSession = Depends(get_db)
):
    stars = await get_stars(db)

    return stars


@router.get(
    "/stars/{star_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
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


@router.patch(
    "/stars/{star_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
)
async def star_update(
    data: NamedEntityUpdateModel,
    star_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    star = await update_star(data, star_id, db)

    if star is None:
        raise HTTPException(
            status_code=404,
            detail="Star not found"
        )

    return star


@router.delete(
    "/stars/{star_id}",
    status_code=200
)
async def star_delete(
    star_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    deleted = await delete_star(star_id, db)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Star not found"
        )

    return {"message": "Star deleted successfully"}


@router.post(
    "/directors",
    status_code=201,
    response_model=NamedEntityResponseModel
)
async def director_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    director = await create_director(data, db)

    return director


@router.get(
    "/directors",
    status_code=200,
    response_model=list[NamedEntityResponseModel]
)
async def directors_list(
    db: AsyncSession = Depends(get_db)
):
    directors = await get_directors(db)

    return directors


@router.get(
    "/directors/{director_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
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


@router.patch(
    "/directors/{director_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
)
async def director_update(
    data: NamedEntityUpdateModel,
    director_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    director = await update_director(
        data,
        director_id,
        db
    )

    if director is None:
        raise HTTPException(
            status_code=404,
            detail="Director not found"
        )

    return director


@router.delete(
    "/directors/{director_id}",
    status_code=200
)
async def director_delete(
    director_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    deleted = await delete_director(
        director_id,
        db
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Director not found"
        )

    return {"message": "Director deleted successfully"}


@router.post(
    "/certifications",
    status_code=201,
    response_model=NamedEntityResponseModel
)
async def certification_create(
    data: NamedEntityCreateModel,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    certification = await create_certification(
        data,
        db
    )

    return certification


@router.get(
    "/certifications",
    status_code=200,
    response_model=list[NamedEntityResponseModel]
)
async def certifications_list(
    db: AsyncSession = Depends(get_db)
):
    certifications = await get_certifications(db)

    return certifications


@router.get(
    "/certifications/{certification_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
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


@router.patch(
    "/certifications/{certification_id}",
    status_code=200,
    response_model=NamedEntityResponseModel
)
async def certification_update(
    data: NamedEntityUpdateModel,
    certification_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    certification = await update_certification(
        data,
        certification_id,
        db
    )

    if certification is None:
        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    return certification


@router.delete(
    "/certifications/{certification_id}",
    status_code=200
)
async def certification_delete(
    certification_id: int,
    db: AsyncSession = Depends(get_db),
    _moderator: User = Depends(require_moderator)
):
    deleted = await delete_certification(
        certification_id,
        db
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    return {
        "message": "Certification deleted successfully"
    }


@router.post(
    "/movies",
    status_code=201,
    response_model=MovieResponseModel
)
async def movie_create(
        data: MovieCreateModel,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
):
    try:
        movie = await create_movie(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return movie


@router.get("/movies", status_code=200, response_model=MovieResponseModel)
async def movies_list(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    movies = get_movies(db, skip, limit)

    return movies
