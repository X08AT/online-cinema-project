import pytest

from app.models.user import UserGroupEnum


@pytest.mark.asyncio
async def test_admin_activate_user_success(
        client,
        inactive_user,
        admin_auth_headers
):
    response = await client.patch(
        f"/admin/users/{inactive_user.id}/activate",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "User activated successfully",
    }


@pytest.mark.asyncio
async def test_admin_activate_user_not_found(client, admin_auth_headers):
    response = await client.patch(
        "/admin/users/1234/activate",
        headers=admin_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found",
    }


@pytest.mark.asyncio
async def test_admin_activate_active_user(
        client,
        active_user,
        admin_auth_headers
):
    response = await client.patch(
        f"/admin/users/{active_user.id}/activate",
        headers=admin_auth_headers,
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "User is already active",
    }


@pytest.mark.asyncio
async def test_admin_activate_user_forbidden(
        client,
        inactive_user,
        auth_headers
):
    response = await client.patch(
        f"/admin/users/{inactive_user.id}/activate",
        headers=auth_headers,
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You are not an admin",
    }


@pytest.mark.asyncio
async def test_admin_update_group_success(
        client,
        active_user,
        admin_auth_headers
):
    response = await client.patch(
        f"/admin/users/{active_user.id}/group",
        headers=admin_auth_headers,
        json={
            "user_group": UserGroupEnum.ADMIN.value,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "User group changed successfully"
    }


@pytest.mark.asyncio
async def test_admin_update_group_user_not_found(client, admin_auth_headers):
    response = await client.patch(
        "/admin/users/1234/group",
        headers=admin_auth_headers,
        json={
            "user_group": UserGroupEnum.ADMIN.value,
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found",
    }


@pytest.mark.asyncio
async def test_admin_update_group_invalid_group(
        client,
        active_user,
        admin_auth_headers
):
    response = await client.patch(
        f"/admin/users/{active_user.id}/group",
        headers=admin_auth_headers,
        json={
            "user_group": "ADMINISTRATOR",
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_admin_update_group_group_not_found(
        client,
        active_user,
        admin_auth_headers
):
    response = await client.patch(
        f"/admin/users/{active_user.id}/group",
        headers=admin_auth_headers,
        json={
            "user_group": UserGroupEnum.MODERATOR.value,
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Group not found",
    }


@pytest.mark.asyncio
async def test_admin_update_group_forbidden(client, active_user, auth_headers):
    response = await client.patch(
        f"/admin/users/{active_user.id}/group",
        headers=auth_headers,
        json={
            "user_group": UserGroupEnum.ADMIN.value,
        }
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You are not an admin",
    }
