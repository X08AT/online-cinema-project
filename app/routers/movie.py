from typing import Literal

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
from app.crud.comment import (
    create_comment,
    get_comments_by_movie_id,
    update_comment, delete_comment
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
from app.crud.movie import (
    create_movie,
    get_movies,
    get_movie_by_id,
    update_movie, delete_movie, get_movies_by_genre
)
from app.crud.reaction import set_movie_reaction, remove_movie_reaction
from app.crud.star import (
    create_star,
    get_stars,
    get_star_by_id,
    update_star,
    delete_star
)
from app.db.dependencies import get_db, require_moderator, get_current_user
from app.models.movie import ReactionEnum
from app.models.user import User
from app.schemas.movie import (
    NamedEntityUpdateModel,
    NamedEntityResponseModel,
    NamedEntityCreateModel,
    MovieResponseModel,
    MovieCreateModel,
    MovieUpdateModel,
    GenreWithCountResponseModel,
    CommentResponseModel,
    CommentCreateModel, CommentUpdateModel
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
    response_model=list[GenreWithCountResponseModel]
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


@router.get(
    "/movies",
    status_code=200,
    response_model=list[MovieResponseModel]
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
    response_model=MovieResponseModel
)
async def movie_get_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@router.patch(
    "/movies/{movie_id}",
    status_code=200,
    response_model=MovieResponseModel
)
async def movie_update(
        movie_id: int,
        data: MovieUpdateModel,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
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
    status_code=200
)
async def movie_delete(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
        _moderator: User = Depends(require_moderator)
):
    deleted = await delete_movie(movie_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"message": "Movie deleted successfully"}


@router.get(
    "/genres/{genre_id}/movies",
    status_code=200,
    response_model=list[MovieResponseModel]
)
async def movie_list_by_genre(
        genre_id: int,
        db: AsyncSession = Depends(get_db)
):
    movies = await get_movies_by_genre(genre_id, db)

    return movies


@router.post("/movies/{movie_id}/like", status_code=201)
async def like_movie(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await set_movie_reaction(movie_id, ReactionEnum.LIKE, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Movie liked successfully"}


@router.post("/movies/{movie_id}/dislike", status_code=201)
async def dislike_movie(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await set_movie_reaction(
            movie_id,
            ReactionEnum.DISLIKE,
            current_user,
            db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Movie disliked successfully"}


@router.delete("/movies/{movie_id}/reaction", status_code=200)
async def delete_movie_reaction(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        deleted = await remove_movie_reaction(movie_id, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not deleted:
        raise HTTPException(status_code=404, detail="Movie reaction not found")

    return {"message": "Movie reaction deleted successfully"}


@router.post(
    "/movies/{movie_id}/comments",
    status_code=201,
    response_model=CommentResponseModel
)
async def comment_movie(
        data: CommentCreateModel,
        movie_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        comment = await create_comment(current_user.id, movie_id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return comment


@router.get(
    "/movies/{movie_id}/comments",
    status_code=200,
    response_model=list[CommentResponseModel]
)
async def movie_comments(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    comments = await get_comments_by_movie_id(movie_id, db)

    return comments


@router.patch(
    "/comments/{comment_id}",
    status_code=200,
    response_model=CommentResponseModel
)
async def comment_update(
        comment_id: int,
        data: CommentUpdateModel,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        comment = await update_comment(comment_id, current_user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return comment


@router.delete(
    "/comments/{comment_id}",
    status_code=200,
)
async def comment_delete(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await delete_comment(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return {"message": "Comment deleted successfully"}
