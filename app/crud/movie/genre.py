from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Genre, MovieGenre
from app.schemas.movie.movie import (
    NamedEntityCreateModel,
    NamedEntityUpdateModel
)


async def create_genre(
        data: NamedEntityCreateModel,
        db: AsyncSession
) -> Genre:
    genre = Genre(**data.model_dump())

    db.add(genre)
    await db.commit()
    await db.refresh(genre)

    return genre


async def get_genres(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(
            Genre,
            func.count(MovieGenre.movie_id)
            .label("movie_count"))
        .outerjoin(MovieGenre, Genre.id == MovieGenre.genre_id)
        .group_by(Genre.id))

    rows = result.all()

    genres = []

    for genre, movie_count in rows:
        genres.append({
            "id": genre.id,
            "name": genre.name,
            "movie_count": movie_count
        })

    return genres


async def get_genre_by_id(genre_id: int, db: AsyncSession) -> Genre | None:
    result = await db.execute(select(Genre).where(Genre.id == genre_id))

    genre = result.scalar_one_or_none()

    return genre


async def update_genre(
        data: NamedEntityUpdateModel,
        genre_id: int,
        db: AsyncSession
) -> Genre | None:
    genre = await get_genre_by_id(genre_id, db)

    if genre is None:
        return None

    genre.name = data.name

    await db.commit()
    await db.refresh(genre)

    return genre


async def delete_genre(genre_id: int, db: AsyncSession) -> bool:
    genre = await get_genre_by_id(genre_id, db)

    if genre is None:
        return False

    await db.delete(genre)
    await db.commit()

    return True
