import pytest


@pytest.mark.asyncio
async def test_add_movie_to_favorites_success(
    client,
    movie,
    auth_headers,
):
    response = await client.post(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_add_movie_to_favorites_not_found(
    client,
    auth_headers,
):
    response = await client.post(
        "/movies/9999/favorite",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_movie_to_favorites_duplicate(
    client,
    movie,
    auth_headers,
):
    first_response = await client.post(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_add_movie_to_favorites_unauthorized(
    client,
    movie,
):
    response = await client.post(
        f"/movies/{movie.id}/favorite"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_favorites_empty(
    client,
    auth_headers,
):
    response = await client.get(
        "/movies/favorites",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_favorites_success(
    client,
    movie,
    auth_headers,
):
    add_response = await client.post(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert add_response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == movie.id
    assert data[0]["name"] == movie.name


@pytest.mark.asyncio
async def test_get_favorites_unauthorized(
    client,
):
    response = await client.get(
        "/movies/favorites"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_multiple_favorites(
    client,
    movies,
    auth_headers,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )

        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_favorites_pagination(
    client,
    movies,
    auth_headers,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={
            "skip": 1,
            "limit": 1,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_favorites_filter_by_year(
    client,
    movies,
    auth_headers,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={"year": 2014},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Interstellar"
    assert data[0]["year"] == 2014


@pytest.mark.asyncio
async def test_favorites_filter_by_imdb(
    client,
    movies,
    auth_headers,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={"imdb": 8.7},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(movie["imdb"] >= 8.7 for movie in data)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_by, expected_first",
    [
        ("price", "Test Cheap Movie"),
        ("year", "Inception"),
        ("votes", "Test Cheap Movie"),
    ],
)
async def test_favorites_sort_ascending(
    client,
    movies,
    auth_headers,
    sort_by,
    expected_first,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={
            "sort_by": sort_by,
            "sort_order": "asc",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == expected_first


@pytest.mark.asyncio
async def test_favorites_sort_price_descending(
    client,
    movies,
    auth_headers,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={
            "sort_by": "price",
            "sort_order": "desc",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Interstellar"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search, expected_movie",
    [
        ("Interstellar", "Interstellar"),
        ("Space exploration", "Interstellar"),
        ("Test Star", "Interstellar"),
        ("Test Director", "Interstellar"),
    ],
)
async def test_search_favorites(
    client,
    movies,
    auth_headers,
    search,
    expected_movie,
):
    for movie in movies:
        response = await client.post(
            f"/movies/{movie.id}/favorite",
            headers=auth_headers,
        )
        assert response.status_code == 201

    response = await client.get(
        "/movies/favorites",
        params={"search": search},
        headers=auth_headers,
    )

    assert response.status_code == 200

    names = [
        movie["name"]
        for movie in response.json()
    ]

    assert expected_movie in names


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"skip": -1},
        {"limit": 0},
        {"limit": 101},
        {"year": 1800},
        {"imdb": -1},
        {"imdb": 11},
        {"sort_by": "invalid"},
        {"sort_order": "invalid"},
    ],
)
async def test_favorites_invalid_query_params(
    client,
    auth_headers,
    params,
):
    response = await client.get(
        "/movies/favorites",
        params=params,
        headers=auth_headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_remove_movie_from_favorites_success(
    client,
    movie,
    auth_headers,
):
    add_response = await client.post(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert add_response.status_code == 201

    response = await client.delete(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_remove_favorite_not_found(
    client,
    movie,
    auth_headers,
):
    response = await client.delete(
        f"/movies/{movie.id}/favorite",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_favorite_movie_not_found(
    client,
    auth_headers,
):
    response = await client.delete(
        "/movies/9999/favorite",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_favorite_unauthorized(
    client,
    movie,
):
    response = await client.delete(
        f"/movies/{movie.id}/favorite"
    )

    assert response.status_code == 401
