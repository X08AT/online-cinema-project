from jose import jwt

from app.core.settings import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def test_hash_password():
    password = "Password123!"

    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_success():
    password = "Password123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_wrong_password():
    hashed = hash_password("Password123!")

    assert verify_password(
        "WrongPassword123!",
        hashed,
    ) is False


def test_create_access_token():
    token = create_access_token(
        {"sub": "123"}
    )

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert payload["sub"] == "123"
    assert "exp" in payload
