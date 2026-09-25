from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, Genre, Star, Director, Certification
from app.schemas.movie import MovieCreateModel


async def create_movie(
        db: AsyncSession,
        data: MovieCreateModel
) -> Movie:
    movie_data = data.model_dump(
        exclude={"genre_ids", "star_ids", "director_ids"}
    )

    movie = Movie(**movie_data)

    result = await db.execute(
        select(Genre)
        .where(Genre.id.in_(data.genre_ids))
    )

    genres = result.scalars().all()

    if len(genres) != len(data.genre_ids):
        raise ValueError("One or more genres do not exist")

    movie.genres = list(genres)

    result = await db.execute(select(Star).where(Star.id.in_(data.star_ids)))

    stars = result.scalars().all()

    if len(stars) != len(data.star_ids):
        raise ValueError("One or more stars do not exist")

    movie.stars = list(stars)

    result = await db.execute(
        select(Director)
        .where(Director.id.in_(data.director_ids))
    )

    directors = result.scalars().all()

    if len(directors) != len(data.director_ids):
        raise ValueError("One or more directors do not exist")

    movie.directors = list(directors)

    result = await db.execute(
        select(Certification)
        .where(Certification.id == data.certification_id)
    )

    certification = result.scalar_one_or_none()

    if certification is None:
        raise ValueError("Certification do not exist")

    db.add(movie)
    await db.commit()
    await db.refresh(movie)

    return movie
