from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, MovieRating
from app.schemas.movie import MovieRatingModel


async def set_movie_rating(
        movie_id: int,
        user_id: int,
        data: MovieRatingModel,
        db: AsyncSession
) -> MovieRating:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    result = await db.execute(
        select(MovieRating)
        .where(
            MovieRating.movie_id == movie_id,
            MovieRating.user_id == user_id
        )
    )

    rating = result.scalar_one_or_none()

    if rating is None:
        rating = MovieRating(
            movie_id=movie.id,
            user_id=user_id,
            **data.model_dump()
        )

        db.add(rating)

    rating.rating = data.rating

    await db.commit()
    await db.refresh(rating)

    return rating
