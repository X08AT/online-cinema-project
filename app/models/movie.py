import uuid
from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy import DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_genres",
        back_populates="genres"
    )


class Star(Base):
    __tablename__ = "stars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_stars",
        back_populates="stars"
    )


class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_directors",
        back_populates="directors"
    )


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        back_populates="certification"
    )


class Movie(Base):
    __tablename__ = "movies"

    __table_args__ = (
        UniqueConstraint("name", "year", "time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    time: Mapped[int] = mapped_column()
    imdb: Mapped[float] = mapped_column()
    votes: Mapped[int] = mapped_column()
    meta_score: Mapped[float | None] = mapped_column()
    gross: Mapped[float | None] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    certification_id: Mapped[int] = mapped_column(
        ForeignKey("certifications.id")
    )

    certification: Mapped[Certification] = relationship(
        "Certification",
        back_populates="movies"
    )
    genres: Mapped[List["Genre"]] = relationship(
        "Genre",
        secondary="movie_genres",
        back_populates="movies"
    )
    stars: Mapped[List["Star"]] = relationship(
        "Star",
        secondary="movie_stars",
        back_populates="movies"
    )
    directors: Mapped[List["Director"]] = relationship(
        "Director",
        secondary="movie_directors",
        back_populates="movies"
    )


class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id"),
        primary_key=True
    )


class MovieStar(Base):
    __tablename__ = "movie_stars"

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        primary_key=True
    )
    star_id: Mapped[int] = mapped_column(
        ForeignKey("stars.id"),
        primary_key=True
    )


class MovieDirector(Base):
    __tablename__ = "movie_directors"

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        primary_key=True
    )
    director_id: Mapped[int] = mapped_column(
        ForeignKey("directors.id"),
        primary_key=True
    )
