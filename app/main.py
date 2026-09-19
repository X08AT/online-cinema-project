from fastapi import FastAPI

from app.routers.auth import router as auth_router

app = FastAPI(title="Online Cinema", version="1.0")

app.include_router(auth_router)