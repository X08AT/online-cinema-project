import pytest


@pytest.mark.asyncio
async def test_get_genres_success(client, genre):
    response = await client.get("/genres")

    assert response.status_code == 200
    assert response.json()[0]["name"] == genre.name


@pytest.mark.asyncio
async def test_get_genre_by_id_success(client, genre):
    response = await client.get(f"/genres/{genre.id}")

    assert response.status_code == 200
    assert response.json()["name"] == genre.name
    assert response.json()["id"] == genre.id


@pytest.mark.asyncio
async def test_get_genre_by_id_not_found(client):
    response = await client.get("/genres/1234")

    assert response.status_code == 404
    assert response.json() == {"detail": "Genre not found"}


@pytest.mark.asyncio
async def test_get_stars_success(client, star):
    response = await client.get("/stars")

    assert response.status_code == 200
    assert response.json()[0]["name"] == star.name


@pytest.mark.asyncio
async def test_get_star_by_id_success(client, star):
    response = await client.get(f"/stars/{star.id}")

    assert response.status_code == 200
    assert response.json()["id"] == star.id
    assert response.json()["name"] == star.name


@pytest.mark.asyncio
async def test_get_star_by_id_not_found(client):
    response = await client.get("/stars/1234")

    assert response.status_code == 404
    assert response.json() == {"detail": "Star not found"}


@pytest.mark.asyncio
async def test_get_directors_success(client, director):
    response = await client.get("/directors")

    assert response.status_code == 200
    assert response.json()[0]["name"] == director.name


@pytest.mark.asyncio
async def test_get_director_by_id_success(client, director):
    response = await client.get(f"/directors/{director.id}")

    assert response.status_code == 200
    assert response.json()["id"] == director.id
    assert response.json()["name"] == director.name


@pytest.mark.asyncio
async def test_get_director_by_id_not_found(client):
    response = await client.get("/directors/1234")

    assert response.status_code == 404
    assert response.json() == {"detail": "Director not found"}


@pytest.mark.asyncio
async def test_get_certifications_success(client, certification):
    response = await client.get("/certifications")

    assert response.status_code == 200
    assert response.json()[0]["name"] == certification.name


@pytest.mark.asyncio
async def test_get_certification_by_id_success(client, certification):
    response = await client.get(f"/certifications/{certification.id}")

    assert response.status_code == 200
    assert response.json()["id"] == certification.id
    assert response.json()["name"] == certification.name


@pytest.mark.asyncio
async def test_get_certification_by_id_not_found(client):
    response = await client.get("/certifications/1234")

    assert response.status_code == 404
    assert response.json() == {"detail": "Certification not found"}


@pytest.mark.asyncio
async def test_get_movies_success(client, movies):
    response = await client.get("/movies")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_movie_by_id_success(client, movie):
    response = await client.get(f"/movies/{movie.id}")

    assert response.status_code == 200
    assert response.json()["id"] == movie.id
    assert response.json()["name"] == movie.name
    assert response.json()["likes_count"] == 0
    assert response.json()["dislikes_count"] == 0


@pytest.mark.asyncio
async def test_get_movie_by_id_not_found(client):
    response = await client.get("/movies/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


@pytest.mark.asyncio
async def test_get_movies_pagination(client, movies):
    response = await client.get(
        "/movies",
        params={
            "skip": 1,
            "limit": 1,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_movies_filter_by_year(client, movies):
    response = await client.get(
        "/movies",
        params={
            "year": 2014,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Interstellar"
    assert response.json()[0]["year"] == 2014


@pytest.mark.asyncio
async def test_get_movies_filter_by_imdb(client, movies):
    response = await client.get(
        "/movies",
        params={
            "imdb": 8.7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(movie["imdb"] >= 8.7 for movie in data)


@pytest.mark.asyncio
async def test_get_movies_sorting_desc(client, movies):
    response = await client.get(
        "/movies",
        params={
            "sort_by": "price",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Interstellar"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_by, expected_first",
    [
        ("price", "Test Cheap Movie"),
        ("year", "Inception"),
        ("votes", "Test Cheap Movie"),
    ],
)
async def test_get_movies_sorting(
    client,
    movies,
    sort_by,
    expected_first,
):
    response = await client.get(
        "/movies",
        params={
            "sort_by": sort_by,
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == expected_first


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
async def test_get_movies_search(
    client,
    movies,
    search,
    expected_movie,
):
    response = await client.get(
        "/movies",
        params={"search": search},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert any(movie["name"] == expected_movie for movie in data)


@pytest.mark.asyncio
async def test_get_movies_by_genre(
    client,
    movies,
    genre,
):
    response = await client.get(f"/genres/{genre.id}/movies")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    assert all(genre["name"] == "Action" for movie in data for genre in movie["genres"])


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
async def test_get_movies_invalid_query_params(
    client,
    params,
):
    response = await client.get(
        "/movies",
        params=params,
    )

    assert response.status_code == 422
