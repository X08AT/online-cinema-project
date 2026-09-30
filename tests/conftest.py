from datetime import datetime, timezone, timedelta, date
from decimal import Decimal

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
from app.models.movie import (
    Genre,
    Director,
    Star,
    Certification,
    Movie,
    MovieComment
)
from app.models.user import (
    UserGroup,
    UserGroupEnum,
    User,
    ActivationToken,
    RefreshToken,
    PasswordResetToken, UserProfile, GenderEnum,
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
            email="active@example.com",
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
async def admin_group():
    async with TestSessionLocal() as session:
        group = UserGroup(
            name=UserGroupEnum.ADMIN.value,
        )

        session.add(group)

        await session.commit()
        await session.refresh(group)

        yield group


@pytest_asyncio.fixture
async def admin_user(admin_group):
    async with TestSessionLocal() as session:
        user = User(
            email="Admin@example.com",
            hashed_password=hash_password("TestPassword123"),
            is_active=True,
            group_id=admin_group.id,
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        yield user


@pytest_asyncio.fixture
async def admin_auth_headers(admin_user):
    access_token = create_access_token({"sub": str(admin_user.id)})

    yield {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture
async def profile(active_user):
    async with TestSessionLocal() as session:
        profile = UserProfile(
            user_id=active_user.id,
            first_name="Test",
            last_name="Profile",
            avatar="test-avatar.jpg",
            gender=GenderEnum.MAN,
            date_of_birth=date(2007, 5, 8),
            info="Test Profile",
        )

        session.add(profile)

        await session.commit()
        await session.refresh(profile)

        yield profile


@pytest_asyncio.fixture
async def genre():
    async with TestSessionLocal() as session:
        genre = Genre(name="Action")

        session.add(genre)
        await session.commit()
        await session.refresh(genre)

        yield genre


@pytest_asyncio.fixture
async def star():
    async with TestSessionLocal() as session:
        star = Star(name="Test Star")

        session.add(star)
        await session.commit()
        await session.refresh(star)

        yield star


@pytest_asyncio.fixture
async def director():
    async with TestSessionLocal() as session:
        director = Director(name="Test Director")

        session.add(director)
        await session.commit()
        await session.refresh(director)

        yield director


@pytest_asyncio.fixture
async def certification():
    async with TestSessionLocal() as session:
        certification = Certification(name="PG-13")

        session.add(certification)
        await session.commit()
        await session.refresh(certification)

        yield certification


@pytest_asyncio.fixture
async def movie(
    genre,
    star,
    director,
    certification,
):
    async with TestSessionLocal() as session:
        genre = await session.merge(genre)
        star = await session.merge(star)
        director = await session.merge(director)
        certification = await session.merge(certification)

        movie = Movie(
            name="Test Movie",
            year=2025,
            time=120,
            imdb=8.5,
            votes=1000,
            meta_score=85,
            gross=1000000,
            description="Test movie description",
            price=Decimal("9.99"),
            certification=certification,
            genres=[genre],
            stars=[star],
            directors=[director],
        )

        session.add(movie)
        await session.commit()
        await session.refresh(movie)

        yield movie


@pytest_asyncio.fixture
async def movies(
    genre,
    star,
    director,
    certification,
):
    async with TestSessionLocal() as session:
        genre = await session.merge(genre)
        star = await session.merge(star)
        director = await session.merge(director)

        movies = [
            Movie(
                name="Interstellar",
                year=2014,
                time=169,
                imdb=8.7,
                votes=2000000,
                meta_score=74,
                gross=700000000,
                description="Space exploration movie",
                price=Decimal("15.99"),
                certification_id=certification.id,
                genres=[genre],
                stars=[star],
                directors=[director],
            ),
            Movie(
                name="Inception",
                year=2010,
                time=148,
                imdb=8.8,
                votes=2500000,
                meta_score=74,
                gross=800000000,
                description="Dream exploration movie",
                price=Decimal("12.99"),
                certification_id=certification.id,
                genres=[genre],
                stars=[star],
                directors=[director],
            ),
            Movie(
                name="Test Cheap Movie",
                year=2020,
                time=100,
                imdb=6.5,
                votes=500,
                meta_score=60,
                gross=100000,
                description="Simple test movie",
                price=Decimal("5.99"),
                certification_id=certification.id,
                genres=[genre],
                stars=[star],
                directors=[director],
            ),
        ]

        session.add_all(movies)
        await session.commit()

        for movie in movies:
            await session.refresh(movie)

        yield movies


@pytest_asyncio.fixture
async def moderator_group():
    async with TestSessionLocal() as session:
        group = UserGroup(
            name=UserGroupEnum.MODERATOR.value
        )

        session.add(group)
        await session.commit()
        await session.refresh(group)

        yield group


@pytest_asyncio.fixture
async def moderator_user(moderator_group):
    async with TestSessionLocal() as session:
        user = User(
            email="moderator@example.com",
            hashed_password=hash_password("Password123!"),
            is_active=True,
            group_id=moderator_group.id,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        yield user


@pytest_asyncio.fixture
async def moderator_auth_headers(moderator_user):
    access_token = create_access_token(
        {"sub": str(moderator_user.id)}
    )

    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest_asyncio.fixture
async def comment(active_user, movie):
    async with TestSessionLocal() as session:
        comment = MovieComment(
            user_id=active_user.id,
            movie_id=movie.id,
            content="Test comment",
        )

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        yield comment


@pytest_asyncio.fixture
async def second_active_user(user_group):
    async with TestSessionLocal() as session:
        user = User(
            email="second@example.com",
            hashed_password=hash_password("Password123!"),
            is_active=True,
            group_id=user_group.id,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        yield user


@pytest_asyncio.fixture
async def second_auth_headers(second_active_user):
    token = create_access_token(
        {"sub": str(second_active_user.id)}
    )

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
