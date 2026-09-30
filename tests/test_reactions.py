import pytest


@pytest.mark.asyncio
async def test_like_movie_success(
    client,
    movie,
    auth_headers,
):
    response = await client.post(
        f"/movies/{movie.id}/like",
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Movie liked successfully"
    }


@pytest.mark.asyncio
async def test_like_movie_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/movies/9999/like",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_like_movie_unauthorized(
    client,
    movie,
):
    response = await client.post(
        f"/movies/{movie.id}/like"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_dislike_movie_success(
    client,
    movie,
    auth_headers,
):
    response = await client.post(
        f"/movies/{movie.id}/dislike",
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Movie disliked successfully"
    }


@pytest.mark.asyncio
async def test_dislike_movie_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/movies/9999/dislike",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dislike_movie_unauthorized(
    client,
    movie,
):
    response = await client.post(
        f"/movies/{movie.id}/dislike"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_like_to_dislike(
    client,
    movie,
    auth_headers,
):
    like_response = await client.post(
        f"/movies/{movie.id}/like",
        headers=auth_headers,
    )

    assert like_response.status_code == 201

    dislike_response = await client.post(
        f"/movies/{movie.id}/dislike",
        headers=auth_headers,
    )

    assert dislike_response.status_code == 201
    assert dislike_response.json() == {
        "message": "Movie disliked successfully"
    }


@pytest.mark.asyncio
async def test_change_dislike_to_like(
    client,
    movie,
    auth_headers,
):
    dislike_response = await client.post(
        f"/movies/{movie.id}/dislike",
        headers=auth_headers,
    )

    assert dislike_response.status_code == 201

    like_response = await client.post(
        f"/movies/{movie.id}/like",
        headers=auth_headers,
    )

    assert like_response.status_code == 201
    assert like_response.json() == {
        "message": "Movie liked successfully"
    }


@pytest.mark.asyncio
async def test_remove_like_success(
    client,
    movie,
    auth_headers,
):
    like_response = await client.post(
        f"/movies/{movie.id}/like",
        headers=auth_headers,
    )

    assert like_response.status_code == 201

    response = await client.delete(
        f"/movies/{movie.id}/reaction",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Movie reaction deleted successfully"
    }


@pytest.mark.asyncio
async def test_remove_dislike_success(
    client,
    movie,
    auth_headers,
):
    dislike_response = await client.post(
        f"/movies/{movie.id}/dislike",
        headers=auth_headers,
    )

    assert dislike_response.status_code == 201

    response = await client.delete(
        f"/movies/{movie.id}/reaction",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Movie reaction deleted successfully"
    }


@pytest.mark.asyncio
async def test_remove_reaction_not_found(
    client,
    movie,
    auth_headers,
):
    response = await client.delete(
        f"/movies/{movie.id}/reaction",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Movie reaction not found"
    }


@pytest.mark.asyncio
async def test_remove_reaction_movie_not_found(
    client,
    auth_headers,
):
    response = await client.delete(
        "/movies/9999/reaction",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_reaction_unauthorized(
    client,
    movie,
):
    response = await client.delete(
        f"/movies/{movie.id}/reaction"
    )

    assert response.status_code == 401
