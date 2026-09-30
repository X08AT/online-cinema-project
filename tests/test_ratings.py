import pytest


@pytest.mark.asyncio
async def test_rate_movie_success(
    client,
    movie,
    auth_headers,
):
    response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 8},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Movie rated successfully"
    }


@pytest.mark.asyncio
async def test_rate_movie_not_found(
    client,
    auth_headers,
):
    response = await client.patch(
        "/movies/9999/rating",
        json={"rating": 8},
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rate_movie_unauthorized(
    client,
    movie,
):
    response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 8},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rating",
    [1, 5, 10],
)
async def test_rate_movie_valid_values(
    client,
    movie,
    auth_headers,
    rating,
):
    response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": rating},
        headers=auth_headers,
    )

    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rating",
    [0, 11, -1, 100],
)
async def test_rate_movie_invalid_values(
    client,
    movie,
    auth_headers,
    rating,
):
    response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": rating},
        headers=auth_headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_rate_movie_missing_rating(
    client,
    movie,
    auth_headers,
):
    response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_movie_rating(
    client,
    movie,
    auth_headers,
):
    first_response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 5},
        headers=auth_headers,
    )

    assert first_response.status_code == 200

    second_response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 9},
        headers=auth_headers,
    )

    assert second_response.status_code == 200
    assert second_response.json() == {
        "message": "Movie rated successfully"
    }


@pytest.mark.asyncio
async def test_get_movie_ratings_success(
    client,
    movie,
    auth_headers,
):
    rate_response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 8},
        headers=auth_headers,
    )

    assert rate_response.status_code == 200

    response = await client.get(
        f"/movies/{movie.id}/ratings",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_get_movie_ratings_without_rating(
    client,
    movie,
    auth_headers,
):
    response = await client.get(
        f"/movies/{movie.id}/ratings",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_get_movie_ratings_not_found(
    client,
    auth_headers,
):
    response = await client.get(
        "/movies/9999/ratings",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_movie_ratings_unauthorized(
    client,
    movie,
):
    response = await client.get(
        f"/movies/{movie.id}/ratings"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_movie_rating_success(
    client,
    movie,
    auth_headers,
):
    rate_response = await client.patch(
        f"/movies/{movie.id}/rating",
        json={"rating": 8},
        headers=auth_headers,
    )

    assert rate_response.status_code == 200

    response = await client.delete(
        f"/movies/{movie.id}/rating",
        headers=auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_movie_rating_not_found(
    client,
    movie,
    auth_headers,
):
    response = await client.delete(
        f"/movies/{movie.id}/rating",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_rating_movie_not_found(
    client,
    auth_headers,
):
    response = await client.delete(
        "/movies/9999/rating",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_movie_rating_unauthorized(
    client,
    movie,
):
    response = await client.delete(
        f"/movies/{movie.id}/rating"
    )

    assert response.status_code == 401
