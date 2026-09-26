from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import MovieComment, Movie
from app.schemas.movie import CommentCreateModel, CommentUpdateModel


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


async def get_comments_by_movie_id(
        movie_id: int,
        db: AsyncSession
) -> list[MovieComment]:
    result = await db.execute(
        select(MovieComment)
        .where(
            MovieComment.movie_id == movie_id,
            MovieComment.parent_id.is_(None)
        )
    )

    comments = result.scalars().all()

    return comments


async def update_comment(
        comment_id: int,
        user_id: int,
        data: CommentUpdateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    if comment.user_id != user_id:
        raise PermissionError("Not your comment")

    comment.content = data.content

    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(
        comment_id: int,
        user_id: int,
        db: AsyncSession
) -> None:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    if comment.user_id != user_id:
        raise PermissionError("Not your comment")

    await db.delete(comment)
    await db.commit()


async def create_reply(
        comment_id: int,
        user_id: int,
        data: CommentCreateModel,
        db: AsyncSession
) -> MovieComment:
    result = await db.execute(
        select(MovieComment)
        .where(MovieComment.id == comment_id)
    )

    comment = result.scalar_one_or_none()

    if comment is None:
        raise ValueError("Comment not found")

    reply = MovieComment(
        user_id=user_id,
        movie_id=comment.movie_id,
        parent_id=comment_id,
        **data.model_dump()
    )
    db.add(reply)
    await db.commit()
    await db.refresh(reply)

    return reply
