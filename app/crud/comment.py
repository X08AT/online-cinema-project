from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import MovieComment, Movie
from app.schemas.movie import CommentCreateModel


async def create_comment(
        user_id: int,
        movie_id: int,
        data: CommentCreateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    movie = result.scalar_one_or_none()

    if movie is None:
        raise ValueError("Movie not found")

    comment = MovieComment(
        user_id=user_id,
        movie_id=movie_id,
        **data.model_dump()
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return comment
