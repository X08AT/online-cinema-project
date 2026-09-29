from fastapi import FastAPI

from app.routers.docs import router as docs_router
from app.routers.movie import router as movie_router
from app.routers.user import router as user_router

app = FastAPI(
    title="Online Cinema",
    version="1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(user_router)
app.include_router(movie_router)
app.include_router(docs_router)
