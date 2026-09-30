import pytest


@pytest.mark.asyncio
async def test_create_comment_success(
    client,
    movie,
    auth_headers,
):
    response = await client.post(
        f"/movies/{movie.id}/comments",
        json={"content": "Great movie!"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["content"] == "Great movie!"


@pytest.mark.asyncio
async def test_create_comment_movie_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/movies/9999/comments",
        json={"content": "Great movie!"},
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_comment_unauthorized(
    client,
    movie,
):
    response = await client.post(
        f"/movies/{movie.id}/comments",
        json={"content": "Great movie!"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_movie_comments_success(
    client,
    movie,
    comment,
):
    response = await client.get(
        f"/movies/{movie.id}/comments"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["content"] == comment.content


@pytest.mark.asyncio
async def test_get_movie_comments_empty(
    client,
    movie,
):
    response = await client.get(
        f"/movies/{movie.id}/comments"
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_update_comment_success(
    client,
    comment,
    auth_headers,
):
    response = await client.patch(
        f"/comments/{comment.id}",
        json={"content": "Updated comment"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated comment"


@pytest.mark.asyncio
async def test_update_comment_not_found(
    client,
    auth_headers,
):
    response = await client.patch(
        "/comments/9999",
        json={"content": "Updated comment"},
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_comment_forbidden(
    client,
    comment,
    second_auth_headers,
):
    response = await client.patch(
        f"/comments/{comment.id}",
        json={"content": "Hacked comment"},
        headers=second_auth_headers,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_comment_success(
    client,
    comment,
    auth_headers,
):
    response = await client.delete(
        f"/comments/{comment.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Comment deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_comment_not_found(
    client,
    auth_headers,
):
    response = await client.delete(
        "/comments/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment_forbidden(
    client,
    comment,
    second_auth_headers,
):
    response = await client.delete(
        f"/comments/{comment.id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_reply_success(
    client,
    comment,
    second_auth_headers,
):
    response = await client.post(
        f"/comments/{comment.id}/replies",
        json={"content": "Test reply"},
        headers=second_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["content"] == "Test reply"


@pytest.mark.asyncio
async def test_create_reply_comment_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/comments/9999/replies",
        json={"content": "Test reply"},
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_like_comment_success(
    client,
    comment,
    second_auth_headers,
):
    response = await client.post(
        f"/comments/{comment.id}/like",
        headers=second_auth_headers,
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Comment liked successfully"
    }


@pytest.mark.asyncio
async def test_like_comment_duplicate(
    client,
    comment,
    second_auth_headers,
):
    first_response = await client.post(
        f"/comments/{comment.id}/like",
        headers=second_auth_headers,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        f"/comments/{comment.id}/like",
        headers=second_auth_headers,
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_like_comment_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/comments/9999/like",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_comment_like_success(
    client,
    comment,
    second_auth_headers,
):
    like_response = await client.post(
        f"/comments/{comment.id}/like",
        headers=second_auth_headers,
    )

    assert like_response.status_code == 201

    response = await client.delete(
        f"/comments/{comment.id}/like",
        headers=second_auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_remove_comment_like_not_found(
    client,
    auth_headers,
):
    response = await client.delete(
        "/comments/9999/like",
        headers=auth_headers,
    )

    assert response.status_code == 404
