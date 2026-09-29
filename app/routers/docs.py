from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.db.dependencies import get_db
from app.models.user import User

router = APIRouter()

security = HTTPBasic()


async def get_docs_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == credentials.username)
    )

    user = result.scalar_one_or_none()

    if (
        user is None
        or not user.is_active
        or not verify_password(
            credentials.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


@router.get("/docs", include_in_schema=False)
async def docs(
    _current_user: User = Depends(get_docs_user),
):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Online Cinema API",
    )


@router.get("/openapi.json", include_in_schema=False)
async def openapi(
    _current_user: User = Depends(get_docs_user),
):
    from app.main import app

    return get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
