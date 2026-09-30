import pytest


@pytest.mark.asyncio
async def test_get_notifications_empty(
    client,
    auth_headers,
):
    response = await client.get(
        "/notifications",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_notifications_success(
    client,
    notification,
    auth_headers,
):
    response = await client.get(
        "/notifications",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == notification.id


@pytest.mark.asyncio
async def test_get_notifications_unauthorized(
    client,
):
    response = await client.get(
        "/notifications"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_read_notification_success(
    client,
    notification,
    auth_headers,
):
    response = await client.patch(
        f"/notifications/{notification.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Notification read successfully"
    }


@pytest.mark.asyncio
async def test_read_notification_not_found(
    client,
    auth_headers,
):
    response = await client.patch(
        "/notifications/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_notification_unauthorized(
    client,
    notification,
):
    response = await client.patch(
        f"/notifications/{notification.id}"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_cannot_read_another_users_notification(
    client,
    notification,
    second_auth_headers,
):
    response = await client.patch(
        f"/notifications/{notification.id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_other_user_does_not_see_notification(
    client,
    notification,
    second_auth_headers,
):
    response = await client.get(
        "/notifications",
        headers=second_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []
