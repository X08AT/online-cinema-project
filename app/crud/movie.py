from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, Genre, Star, Director, Certification
from app.schemas.movie import MovieCreateModel, MovieUpdateModel


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


async def get_movies(
        db: AsyncSession,
        skip: int,
        limit: int,
        year: int | None = None,
        imdb: float | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc"
) -> list[Movie]:
    query = select(Movie)

    if year is not None:
        query = query.where(Movie.year == year)

    if imdb is not None:
        query = query.where(Movie.imdb >= imdb)

    sort_fields = {
        "price": Movie.price,
        "year": Movie.year,
        "votes": Movie.votes,
    }

    sort_colum = sort_fields.get(sort_by)

    if sort_colum is not None:
        if sort_order == "desc":
            query = query.order_by(sort_colum.desc())
        else:
            query = query.order_by(sort_colum.asc())

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    movies = result.scalars().all()

    return movies


async def get_movie_by_id(movie_id: int, db: AsyncSession) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = result.scalar_one_or_none()

    return movie


async def update_movie(
        data: MovieUpdateModel,
        movie_id: int,
        db: AsyncSession
) -> Movie | None:
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        return None

    update_data = data.model_dump(
        exclude_unset=True,
        exclude={"genre_ids", "star_ids", "director_ids", "certification_id"}
    )

    for field, value in update_data.items():
        setattr(movie, field, value)

    if data.genre_ids is not None:
        result = await db.execute(
            select(Genre)
            .where(Genre.id.in_(data.genre_ids))
        )
        genres = result.scalars().all()
        if len(genres) != len(data.genre_ids):
            raise ValueError("One or more genres do not exist")
        movie.genres = list(genres)

    if data.star_ids is not None:
        result = await db.execute(
            select(Star)
            .where(Star.id.in_(data.star_ids))
        )
        stars = result.scalars().all()
        if len(stars) != len(data.star_ids):
            raise ValueError("One or more stars do not exist")
        movie.stars = list(stars)

    if data.director_ids is not None:
        result = await db.execute(
            select(Director)
            .where(Director.id.in_(data.director_ids))
        )
        directors = result.scalars().all()
        if len(directors) != len(data.director_ids):
            raise ValueError("One or more directors do not exist")
        movie.directors = list(directors)

    if data.certification_id is not None:
        result = await db.execute(
            select(Certification)
            .where(Certification.id == data.certification_id)
        )
        certification = result.scalar_one_or_none()
        if certification is None:
            raise ValueError("Certification does not exist")
        movie.certification = certification

    await db.commit()
    await db.refresh(movie)

    return movie


async def delete_movie(movie_id: int, db: AsyncSession) -> bool:
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        return False

    await db.delete(movie)
    await db.commit()

    return True
