import pytest

from app.models.user import GenderEnum


@pytest.mark.asyncio
async def test_create_profile_success(
        client,
        auth_headers,
        monkeypatch,
):
    monkeypatch.setattr(
        "app.routers.user.profile.upload_avatar",
        lambda avatar: "test-avatar.jpg",
    )

    response = await client.post(
        "/profile",
        headers=auth_headers,
        data={
            "first_name": "Test",
            "last_name": "Profile",
            "gender": GenderEnum.MAN.value,
            "date_of_birth": "2007-05-08",
            "info": "Test Profile",
        },
        files={
            "avatar": (
                "test-avatar.jpg",
                b"fake image content",
                "image/jpeg",
            )
        }
    )

    assert response.status_code == 201
    assert response.json()["first_name"] == "Test"
    assert response.json()["avatar"] == "test-avatar.jpg"


@pytest.mark.asyncio
async def test_create_profile_already_exists(
        client,
        auth_headers,
        monkeypatch,
):
    monkeypatch.setattr(
        "app.routers.user.profile.upload_avatar",
        lambda avatar: "test-avatar.jpg",
    )

    response = await client.post(
        "/profile",
        headers=auth_headers,
        data={
            "first_name": "Test",
            "last_name": "Profile",
            "gender": GenderEnum.MAN.value,
            "date_of_birth": "2007-05-08",
            "info": "Test Profile",
        },
        files={
            "avatar": (
                "test-avatar.jpg",
                b"fake image content",
                "image/jpeg",
            )
        }
    )

    assert response.status_code == 201

    response = await client.post(
        "/profile",
        headers=auth_headers,
        data={
            "first_name": "Test",
            "last_name": "Profile",
            "gender": GenderEnum.MAN.value,
            "date_of_birth": "2007-05-08",
            "info": "Test Profile",
        },
        files={
            "avatar": (
                "test-avatar.jpg",
                b"fake image content",
                "image/jpeg",
            )
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Profile already created",
    }


@pytest.mark.asyncio
async def test_get_profile_success(
        client,
        profile,
        auth_headers,
):
    response = await client.get(
        "/profile",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"
    assert response.json()["avatar"] == "test-avatar.jpg"


@pytest.mark.asyncio
async def test_get_profile_not_found(client, auth_headers):
    response = await client.get(
        "/profile",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Profile not found"
    }


@pytest.mark.asyncio
async def test_update_profile_success(client, profile, auth_headers):
    response = await client.patch(
        "/profile",
        headers=auth_headers,
        data={
            "first_name": "NewTest",
            "info": "Updated Profile",
        }
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == "NewTest"
    assert response.json()["info"] == "Updated Profile"


@pytest.mark.asyncio
async def test_update_profile_not_found(client, auth_headers):
    response = await client.patch(
        "/profile",
        headers=auth_headers,
        data={
            "first_name": "NewTest",
            "info": "Updated Profile",
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Profile not found"
    }


@pytest.mark.asyncio
async def test_update_profile_with_avatar(
        client,
        profile,
        auth_headers,
        monkeypatch
):
    monkeypatch.setattr(
        "app.routers.user.profile.upload_avatar",
        lambda avatar: "new-avatar.jpg",
    )

    response = await client.patch(
        "/profile",
        headers=auth_headers,
        files={
            "avatar": (
                "new-avatar.jpg",
                b"fake image content",
                "image/jpeg",
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["avatar"] == "new-avatar.jpg"
