from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.movie import Movie, Genre, Star, Director, Certification
from app.schemas.movie.movie import MovieUpdateModel, MovieCreateModel


async def create_movie(db: AsyncSession, data: MovieCreateModel) -> Movie:
    movie_data = data.model_dump(exclude={"genre_ids", "star_ids", "director_ids"})

    movie = Movie(**movie_data)

    genre_result = await db.execute(select(Genre).where(Genre.id.in_(data.genre_ids)))
    genres = genre_result.scalars().all()

    if len(genres) != len(data.genre_ids):
        raise ValueError("One or more genres do not exist")

    movie.genres = list(genres)

    star_result = await db.execute(select(Star).where(Star.id.in_(data.star_ids)))
    stars = star_result.scalars().all()

    if len(stars) != len(data.star_ids):
        raise ValueError("One or more stars do not exist")

    movie.stars = list(stars)

    director_result = await db.execute(
        select(Director).where(Director.id.in_(data.director_ids))
    )
    directors = director_result.scalars().all()

    if len(directors) != len(data.director_ids):
        raise ValueError("One or more directors do not exist")

    movie.directors = list(directors)

    certification_result = await db.execute(
        select(Certification).where(Certification.id == data.certification_id)
    )
    certification = certification_result.scalar_one_or_none()

    if certification is None:
        raise ValueError("Certification does not exist")

    db.add(movie)
    await db.commit()

    created_movie = await get_movie_by_id(movie.id, db)

    if created_movie is None:
        raise ValueError("Movie not found after creation")

    return created_movie


async def get_movies(
    db: AsyncSession,
    skip: int,
    limit: int,
    year: int | None = None,
    imdb: float | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    search: str | None = None,
) -> list[Movie]:
    query = select(Movie).options(
        selectinload(Movie.certification),
        selectinload(Movie.genres),
        selectinload(Movie.stars),
        selectinload(Movie.directors),
        selectinload(Movie.reactions),
    )

    if year is not None:
        query = query.where(Movie.year == year)

    if imdb is not None:
        query = query.where(Movie.imdb >= imdb)

    sort_fields = {
        "price": Movie.price,
        "year": Movie.year,
        "votes": Movie.votes,
    }

    sort_column = sort_fields.get(sort_by) if sort_by is not None else None

    if sort_column is not None:
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    if search is not None:
        query = query.where(
            or_(
                Movie.name.ilike(f"%{search}%"),
                Movie.description.ilike(f"%{search}%"),
                Movie.stars.any(Star.name.ilike(f"%{search}%")),
                Movie.directors.any(Director.name.ilike(f"%{search}%")),
            )
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    movies = result.scalars().all()

    return list(movies)


async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession,
) -> Movie | None:
    result = await db.execute(
        select(Movie)
        .options(
            selectinload(Movie.certification),
            selectinload(Movie.genres),
            selectinload(Movie.stars),
            selectinload(Movie.directors),
            selectinload(Movie.reactions),
        )
        .where(Movie.id == movie_id)
    )

    movie = result.scalar_one_or_none()

    return movie


async def update_movie(
    data: MovieUpdateModel,
    movie_id: int,
    db: AsyncSession,
) -> Movie | None:
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        return None

    update_data = data.model_dump(
        exclude_unset=True,
        exclude={
            "genre_ids",
            "star_ids",
            "director_ids",
            "certification_id",
        },
    )

    for field, value in update_data.items():
        setattr(movie, field, value)

    if data.genre_ids is not None:
        genre_result = await db.execute(
            select(Genre).where(Genre.id.in_(data.genre_ids))
        )
        genres = genre_result.scalars().all()

        if len(genres) != len(data.genre_ids):
            raise ValueError("One or more genres do not exist")

        movie.genres = list(genres)

    if data.star_ids is not None:
        star_result = await db.execute(select(Star).where(Star.id.in_(data.star_ids)))
        stars = star_result.scalars().all()

        if len(stars) != len(data.star_ids):
            raise ValueError("One or more stars do not exist")

        movie.stars = list(stars)

    if data.director_ids is not None:
        director_result = await db.execute(
            select(Director).where(Director.id.in_(data.director_ids))
        )
        directors = director_result.scalars().all()

        if len(directors) != len(data.director_ids):
            raise ValueError("One or more directors do not exist")

        movie.directors = list(directors)

    if data.certification_id is not None:
        certification_result = await db.execute(
            select(Certification).where(Certification.id == data.certification_id)
        )
        certification = certification_result.scalar_one_or_none()

        if certification is None:
            raise ValueError("Certification does not exist")

        movie.certification = certification

    await db.commit()

    return await get_movie_by_id(movie.id, db)


async def delete_movie(
    movie_id: int,
    db: AsyncSession,
) -> bool:
    movie = await get_movie_by_id(movie_id, db)

    if movie is None:
        return False

    await db.delete(movie)
    await db.commit()

    return True


async def get_movies_by_genre(
    genre_id: int,
    db: AsyncSession,
) -> list[Movie]:
    result = await db.execute(
        select(Movie)
        .options(
            selectinload(Movie.certification),
            selectinload(Movie.genres),
            selectinload(Movie.stars),
            selectinload(Movie.directors),
            selectinload(Movie.reactions),
        )
        .where(Movie.genres.any(Genre.id == genre_id))
    )

    movies = result.scalars().all()

    return list(movies)
