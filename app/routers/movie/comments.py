from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie.comment import (
    remove_like,
    create_reply,
    delete_comment,
    update_comment,
    like_comment,
    create_comment,
    get_comments_by_movie_id
)
from app.db.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.movie.comment import (
    CommentResponseModel,
    CommentCreateModel,
    ReplyResponseModel,
    CommentUpdateModel
)

router = APIRouter(tags=["Comments"])


@router.post(
    "/movies/{movie_id}/comments",
    status_code=201,
    response_model=CommentResponseModel,
    summary="Add comment to movie",
    description=(
        "Creates a new comment for the specified movie. "
        "The user must be authenticated."
    ),
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
    response_model=list[CommentResponseModel],
    summary="Get movie comments",
    description=(
        "Returns all comments associated with the specified movie."
    ),
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
    response_model=CommentResponseModel,
    summary="Update comment",
    description=(
        "Updates an existing comment. "
        "Only the author of the comment can update it."
    ),
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
    summary="Delete comment",
    description=(
        "Deletes an existing comment. "
        "Only the author of the comment can delete it."
    ),
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


@router.post(
    "/comments/{comment_id}/replies",
    status_code=201,
    response_model=ReplyResponseModel,
    summary="Reply to comment",
    description=(
        "Creates a reply to the specified comment. "
        "The user must be authenticated."
    ),
)
async def reply_on_comment(
        comment_id: int,
        data: CommentCreateModel,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        reply = await create_reply(comment_id, current_user.id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return reply


@router.post(
    "/comments/{comment_id}/like",
    status_code=201,
    summary="Like comment",
    description=(
        "Adds a like from the authenticated user to the specified comment."
    ),
)
async def comment_like(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await like_comment(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {"message": "Comment liked successfully"}


@router.delete(
    "/comments/{comment_id}/like",
    status_code=204,
    summary="Remove comment like",
    description=(
        "Removes the authenticated user's like from the specified comment."
    ),
)
async def remove_comment_like(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        await remove_like(comment_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
