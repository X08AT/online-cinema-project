import pytest


@pytest.mark.asyncio
async def test_create_genre_success(
    client,
    moderator_auth_headers,
):
    response = await client.post(
        "/genres",
        json={"name": "Comedy"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Comedy"


@pytest.mark.asyncio
async def test_update_genre_success(
    client,
    genre,
    moderator_auth_headers,
):
    response = await client.patch(
        f"/genres/{genre.id}",
        json={"name": "Drama"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Drama"


@pytest.mark.asyncio
async def test_update_genre_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.patch(
        "/genres/9999",
        json={"name": "Drama"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Genre not found"
    }


@pytest.mark.asyncio
async def test_delete_genre_success(
    client,
    genre,
    moderator_auth_headers,
):
    response = await client.delete(
        f"/genres/{genre.id}",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Genre deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_genre_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.delete(
        "/genres/9999",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Genre not found"
    }


@pytest.mark.asyncio
async def test_create_genre_forbidden(
    client,
    auth_headers,
):
    response = await client.post(
        "/genres",
        json={"name": "Comedy"},
        headers=auth_headers,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_star_success(
    client,
    moderator_auth_headers,
):
    response = await client.post(
        "/stars",
        json={"name": "New Star"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "New Star"


@pytest.mark.asyncio
async def test_update_star_success(
    client,
    star,
    moderator_auth_headers,
):
    response = await client.patch(
        f"/stars/{star.id}",
        json={"name": "Updated Star"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Star"


@pytest.mark.asyncio
async def test_update_star_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.patch(
        "/stars/9999",
        json={"name": "Updated Star"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Star not found"
    }


@pytest.mark.asyncio
async def test_delete_star_success(
    client,
    star,
    moderator_auth_headers,
):
    response = await client.delete(
        f"/stars/{star.id}",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Star deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_star_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.delete(
        "/stars/9999",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Star not found"
    }


@pytest.mark.asyncio
async def test_create_director_success(
    client,
    moderator_auth_headers,
):
    response = await client.post(
        "/directors",
        json={"name": "New Director"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "New Director"


@pytest.mark.asyncio
async def test_update_director_success(
    client,
    director,
    moderator_auth_headers,
):
    response = await client.patch(
        f"/directors/{director.id}",
        json={"name": "Updated Director"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Director"


@pytest.mark.asyncio
async def test_update_director_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.patch(
        "/directors/9999",
        json={"name": "Updated Director"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Director not found"
    }


@pytest.mark.asyncio
async def test_delete_director_success(
    client,
    director,
    moderator_auth_headers,
):
    response = await client.delete(
        f"/directors/{director.id}",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Director deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_director_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.delete(
        "/directors/9999",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Director not found"
    }


@pytest.mark.asyncio
async def test_create_certification_success(
    client,
    moderator_auth_headers,
):
    response = await client.post(
        "/certifications",
        json={"name": "R"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "R"


@pytest.mark.asyncio
async def test_update_certification_success(
    client,
    certification,
    moderator_auth_headers,
):
    response = await client.patch(
        f"/certifications/{certification.id}",
        json={"name": "R"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "R"


@pytest.mark.asyncio
async def test_update_certification_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.patch(
        "/certifications/9999",
        json={"name": "R"},
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Certification not found"
    }


@pytest.mark.asyncio
async def test_delete_certification_success(
    client,
    certification,
    moderator_auth_headers,
):
    response = await client.delete(
        f"/certifications/{certification.id}",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Certification deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_certification_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.delete(
        "/certifications/9999",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Certification not found"
    }


@pytest.mark.asyncio
async def test_create_movie_success(
    client,
    genre,
    star,
    director,
    certification,
    moderator_auth_headers,
):
    response = await client.post(
        "/movies",
        json={
            "name": "New Movie",
            "year": 2026,
            "time": 120,
            "imdb": 8.0,
            "votes": 1000,
            "meta_score": 80,
            "gross": 1000000,
            "description": "New movie description",
            "price": "10.99",
            "certification_id": certification.id,
            "genre_ids": [genre.id],
            "star_ids": [star.id],
            "director_ids": [director.id],
        },
        headers=moderator_auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "New Movie"
    assert data["year"] == 2026
    assert data["certification"]["id"] == certification.id
    assert data["genres"][0]["id"] == genre.id
    assert data["stars"][0]["id"] == star.id
    assert data["directors"][0]["id"] == director.id


@pytest.mark.asyncio
async def test_create_movie_invalid_data(
    client,
    genre,
    star,
    director,
    certification,
    moderator_auth_headers,
):
    response = await client.post(
        "/movies",
        json={
            "name": "Invalid Movie",
            "year": 2026,
            "time": 120,
            "imdb": 11,
            "votes": 1000,
            "description": "Invalid movie",
            "price": "10.99",
            "certification_id": certification.id,
            "genre_ids": [genre.id],
            "star_ids": [star.id],
            "director_ids": [director.id],
        },
        headers=moderator_auth_headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_movie_invalid_relation(
    client,
    genre,
    star,
    director,
    certification,
    moderator_auth_headers,
):
    response = await client.post(
        "/movies",
        json={
            "name": "Invalid Relation Movie",
            "year": 2026,
            "time": 120,
            "imdb": 8.0,
            "votes": 1000,
            "meta_score": 80,
            "gross": 1000000,
            "description": "Movie with invalid genre",
            "price": "10.99",
            "certification_id": certification.id,
            "genre_ids": [9999],
            "star_ids": [star.id],
            "director_ids": [director.id],
        },
        headers=moderator_auth_headers,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_movie_success(
    client,
    movie,
    moderator_auth_headers,
):
    response = await client.patch(
        f"/movies/{movie.id}",
        json={
            "name": "Updated Movie",
            "price": "19.99",
        },
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Movie"
    assert data["price"] == "19.99"


@pytest.mark.asyncio
async def test_update_movie_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.patch(
        "/movies/9999",
        json={
            "name": "Updated Movie",
        },
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Movie not found"
    }


@pytest.mark.asyncio
async def test_delete_movie_success(
    client,
    movie,
    moderator_auth_headers,
):
    response = await client.delete(
        f"/movies/{movie.id}",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Movie deleted successfully"
    }


@pytest.mark.asyncio
async def test_delete_movie_not_found(
    client,
    moderator_auth_headers,
):
    response = await client.delete(
        "/movies/9999",
        headers=moderator_auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Movie not found"
    }


@pytest.mark.asyncio
async def test_create_movie_forbidden(
    client,
    genre,
    star,
    director,
    certification,
    auth_headers,
):
    response = await client.post(
        "/movies",
        json={
            "name": "Forbidden Movie",
            "year": 2026,
            "time": 120,
            "imdb": 8.0,
            "votes": 1000,
            "description": "Forbidden movie",
            "price": "10.99",
            "certification_id": certification.id,
            "genre_ids": [genre.id],
            "star_ids": [star.id],
            "director_ids": [director.id],
        },
        headers=auth_headers,
    )

    assert response.status_code == 403
