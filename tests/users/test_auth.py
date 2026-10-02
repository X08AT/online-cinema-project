import pytest


@pytest.mark.asyncio
async def test_register_success(client, user_group, monkeypatch):
    monkeypatch.setattr(
        "app.routers.user.auth.send_email",
        lambda *args, **kwargs: None,
    )

    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "Password123"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": (
            "Registration successful. " "Check your email to activate your account."
        )
    }


@pytest.mark.asyncio
async def test_register_duplicate_email(client, user_group, monkeypatch):
    monkeypatch.setattr(
        "app.routers.user.auth.send_email",
        lambda *args, **kwargs: None,
    )

    response = await client.post(
        "/auth/register", json={"email": "test@example.com", "password": "Password123"}
    )

    assert response.status_code == 201

    response = await client.post(
        "/auth/register", json={"email": "test@example.com", "password": "Password123"}
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "password", ["Pass1", "password123", "PASSWORD123", "Password", "Password123aaaaaa"]
)
async def test_register_invalid_password(client, password):
    response = await client.post(
        "/auth/register", json={"email": "test@example.com", "password": password}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post(
        "/auth/register", json={"email": "test", "password": "Test123"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_activate_user_success(client, inactive_user, activation_token):
    response = await client.get(
        "/auth/activate", params={"token": activation_token.token}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Account activated"}


@pytest.mark.asyncio
async def test_activate_invalid_token(client):
    response = await client.get("/auth/activate", params={"token": "wrong-token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Token does not exist"}


@pytest.mark.asyncio
async def test_expired_activation_token(client, expired_activation_token):
    response = await client.get(
        "/auth/activate", params={"token": expired_activation_token.token}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Activation token has expired"}


@pytest.mark.asyncio
async def test_resend_activation_success(client, inactive_user, monkeypatch):
    monkeypatch.setattr(
        "app.routers.user.auth.send_email",
        lambda *args, **kwargs: None,
    )

    response = await client.post(
        "/auth/resend-activation",
        json={
            "email": inactive_user.email,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Activation email sent"}


@pytest.mark.asyncio
async def test_resend_activation_user_not_found(client):
    response = await client.post(
        "/auth/resend-activation",
        json={
            "email": "WrongEmail@example.com",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


@pytest.mark.asyncio
async def test_resend_activation_user_is_active(client, active_user):
    response = await client.post(
        "/auth/resend-activation",
        json={
            "email": active_user.email,
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User is already active"}


@pytest.mark.asyncio
async def test_login_success(client, active_user):
    response = await client.post(
        "/auth/login", json={"email": active_user.email, "password": "TestPassword123"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_incorrect_password(client, active_user):
    response = await client.post(
        "/auth/login", json={"email": active_user.email, "password": "WrongPass123"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


@pytest.mark.asyncio
async def test_login_inactive_user(client, inactive_user):
    response = await client.post(
        "/auth/login",
        json={"email": inactive_user.email, "password": "TestPassword123"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "User is not active"}


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post(
        "/auth/login",
        json={"email": "WrongEmail@example.com", "password": "WrongPassword123"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


@pytest.mark.asyncio
async def test_refresh_token_success(client, refresh_token):
    response = await client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token.token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_invalid_refresh_token(client):
    response = await client.post(
        "/auth/refresh",
        json={
            "refresh_token": "wrong-refresh-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid refresh token"}


@pytest.mark.asyncio
async def test_expired_refresh_token(client, expired_refresh_token):
    response = await client.post(
        "/auth/refresh",
        json={
            "refresh_token": expired_refresh_token.token,
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Refresh token has expired"}


@pytest.mark.asyncio
async def test_logout_success(client, refresh_token):
    response = await client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token.token,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "You have been logged out"}


@pytest.mark.asyncio
async def test_logout_invalid_refresh_token(client):
    response = await client.post(
        "/auth/logout",
        json={
            "refresh_token": "wrong-refresh-token",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Refresh token does not exist"}


@pytest.mark.asyncio
async def test_change_password_success(client, active_user, auth_headers):
    response = await client.post(
        "/auth/change-password",
        headers=auth_headers,
        json={
            "old_password": "TestPassword123",
            "password": "NewPassword123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Password changed"}


@pytest.mark.asyncio
async def test_change_password_incorrect_old_password(
    client, active_user, auth_headers
):
    response = await client.post(
        "/auth/change-password",
        headers=auth_headers,
        json={
            "old_password": "WrongPassword123",
            "password": "NewPassword123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect old password"}


@pytest.mark.asyncio
async def test_password_reset_request_success(client, active_user, monkeypatch):
    monkeypatch.setattr(
        "app.routers.user.auth.send_email",
        lambda *args, **kwargs: None,
    )

    response = await client.post(
        "/auth/password-reset/request",
        json={
            "email": active_user.email,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Password reset link sent to your email"}


@pytest.mark.asyncio
async def test_password_reset_request_invalid_user(client):
    response = await client.post(
        "/auth/password-reset/request",
        json={
            "email": "WrongEmail@example.com",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


@pytest.mark.asyncio
async def test_password_reset_request_inactive_user(client, inactive_user):
    response = await client.post(
        "/auth/password-reset/request",
        json={
            "email": inactive_user.email,
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "User is not active"}


@pytest.mark.asyncio
async def test_password_reset_success(client, password_reset_token):
    response = await client.post(
        "/auth/password-reset/confirm",
        params={"token": password_reset_token.token},
        json={
            "new_password": "NewPass123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Password reset successfully"}


@pytest.mark.asyncio
async def test_password_reset_invalid_token(client):
    response = await client.post(
        "/auth/password-reset/confirm",
        params={"token": "InvalidToken"},
        json={
            "new_password": "NewPass123",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Password reset token does not exist"}


@pytest.mark.asyncio
async def test_password_reset_expired_token(client, expired_password_reset_token):
    response = await client.post(
        "/auth/password-reset/confirm",
        params={"token": expired_password_reset_token.token},
        json={
            "new_password": "NewPass123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Password reset token expired"}


@pytest.mark.asyncio
async def test_password_reset_inactive_user(client, inactive_user_password_reset_token):
    response = await client.post(
        "/auth/password-reset/confirm",
        params={"token": inactive_user_password_reset_token.token},
        json={
            "new_password": "NewPass123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "User is not active"}
