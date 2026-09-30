from datetime import datetime, timezone, timedelta

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.security import hash_password, create_access_token
from app.core.settings import settings
from app.db.dependencies import get_db
from app.db.session import Base
from app.main import app
from app.models.user import (
    UserGroup,
    UserGroupEnum,
    User,
    ActivationToken,
    RefreshToken,
    PasswordResetToken,
)

test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def create_test_tables():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user_group():
    async with TestSessionLocal() as session:
        group = UserGroup(name=UserGroupEnum.USER.value)

        session.add(group)
        await session.commit()

        yield group


@pytest_asyncio.fixture
async def inactive_user(user_group):
    async with TestSessionLocal() as session:
        user = User(
            email="test@example.com",
            hashed_password="TestPassword123",
            is_active=False,
            group_id=user_group.id,
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        yield user


@pytest_asyncio.fixture
async def active_user(user_group):
    async with TestSessionLocal() as session:
        hashed_password = hash_password("TestPassword123")
        user = User(
            email="test@example.com",
            hashed_password=hashed_password,
            is_active=True,
            group_id=user_group.id,
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        yield user


@pytest_asyncio.fixture
async def activation_token(inactive_user):
    async with TestSessionLocal() as session:
        token = ActivationToken(
            user_id=inactive_user.id,
            token="TestToken123",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def expired_activation_token(inactive_user):
    async with TestSessionLocal() as session:
        token = ActivationToken(
            user_id=inactive_user.id,
            token="TestToken123",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def refresh_token(active_user):
    async with TestSessionLocal() as session:
        token = RefreshToken(
            user_id=active_user.id,
            token="TestRefreshToken123",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def expired_refresh_token(active_user):
    async with TestSessionLocal() as session:
        token = RefreshToken(
            user_id=active_user.id,
            token="TestRefreshToken123",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def auth_headers(active_user):
    access_token = create_access_token({"sub": str(active_user.id)})

    yield {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture
async def password_reset_token(active_user):
    async with TestSessionLocal() as session:
        token = PasswordResetToken(
            user_id=active_user.id,
            token="TestPasswordResetToken123",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def expired_password_reset_token(active_user):
    async with TestSessionLocal() as session:
        token = PasswordResetToken(
            user_id=active_user.id,
            token="TestPasswordResetToken123",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def inactive_user_password_reset_token(inactive_user):
    async with TestSessionLocal() as session:
        token = PasswordResetToken(
            user_id=inactive_user.id,
            token="TestPasswordResetToken123",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

        session.add(token)

        await session.commit()
        await session.refresh(token)

        yield token


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
