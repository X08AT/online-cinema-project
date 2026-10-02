# 🎬 Online Cinema API

Online Cinema is a backend REST API for an online movie platform built with **FastAPI**.

The application provides user authentication and authorization, role-based access control, movie catalog management, favorites, ratings, comments, notifications, and administrative features.

The project is containerized with Docker, covered with automated tests, deployed on AWS EC2, and uses GitHub Actions for automated CI/CD.

## ✨ Features

### 🔐 Authentication & Users

- User registration with email activation
- Account activation via email link
- Resending activation emails
- JWT authentication with access and refresh tokens
- Access token refreshing
- Logout with refresh token invalidation
- Password change
- Password reset via email
- Password complexity validation
- User profiles
- Role-based access control

Available roles:

- `USER`
- `MODERATOR`
- `ADMIN`

### 🎥 Movies

- Browse movies with pagination
- View detailed movie information
- Search movies
- Filter movies
- Sort movies
- Movie genres
- Actors
- Directors
- Certifications
- Like and dislike movies
- Rate movies
- Comments and replies
- Notifications for user interactions

Moderators have additional permissions for managing movie-related content.

### ❤️ Favorites

Authenticated users can maintain their own list of favorite movies.

Supported functionality includes:

- Add movies to favorites
- Remove movies from favorites
- View favorite movies
- Search favorites
- Filter favorites
- Sort favorites
- Prevent duplicate favorite entries

### ⭐ Ratings & Reactions

Users can interact with movies through:

- Ratings
- Likes
- Dislikes

### 💬 Comments & Notifications

Users can interact with movie content through comments and replies.

The application also supports notifications related to user interactions.

### 👥 Role-Based Access Control

The application provides three user roles with different permission levels.

#### USER

Regular users can browse and interact with the movie catalog and use user-facing functionality.

#### MODERATOR

Moderators have additional permissions for managing movie-related content.

#### ADMIN

Administrators have extended permissions for managing users and application data.

---

## 🛠 Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic

### Database & Storage

- PostgreSQL
- Redis
- MinIO

### Background Processing

- Celery
- Celery Beat

### Testing & Code Quality

- Pytest
- pytest-cov
- Black
- Flake8
- mypy

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- AWS EC2

---

## 🌐 Live Deployment

The application is deployed on **AWS EC2** and is publicly available.

- **API:** http://13.53.199.202:8000
- **Swagger UI:** http://13.53.199.202:8000/docs
- **OpenAPI Schema:** http://13.53.199.202:8000/openapi.json

### 🔑 Swagger Access

Swagger UI is protected with authentication.

Use the following demo credentials to access the API documentation:

```text
Email: user@example.com
Password: User1234
```

Additional demo accounts with different roles are available in the **Demo Accounts** section below.

---

## 🐳 Running the Project with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/X08AT/online-cinema-project.git
cd online-cinema-project
```

### 2. Configure Environment Variables

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Update the values in `.env` if necessary.

In particular, use a secure value for:

```env
SECRET_KEY=your-secret-key
```

You can generate a secure secret key with:

```bash
openssl rand -hex 32
```

### 3. Start the Application

```bash
docker compose up --build -d
```

Docker Compose starts the required services, including:

- FastAPI application
- PostgreSQL
- Redis
- MinIO
- Celery worker
- Celery Beat
- MailHog
- Database migrations
- Demo user seeding

### 4. Check Running Containers

```bash
docker compose ps
```

To also see completed services such as database migrations and user seeding:

```bash
docker compose ps -a
```

### 5. Stop the Application

```bash
docker compose down
```

---

## 👤 Demo Accounts

Demo accounts are automatically created by the seed service.

| Role | Email | Password |
| --- | --- | --- |
| User | `user@example.com` | `User1234` |
| Moderator | `moderator@example.com` | `Moderator123` |
| Admin | `admin@example.com` | `Admin1234` |

These accounts can be used to test different permission levels and API functionality.

The seed process is idempotent, so restarting the application does not create duplicate demo users.

---

## 📖 API Documentation

### Local

When the application is running locally, interactive Swagger UI documentation is available at:

```text
http://localhost:8000/docs
```

The raw OpenAPI schema is available at:

```text
http://localhost:8000/openapi.json
```

### Deployed

The deployed API documentation is available at:

```text
http://13.53.199.202:8000/docs
```

OpenAPI schema:

```text
http://13.53.199.202:8000/openapi.json
```

Use one of the demo accounts above to authenticate and test the available endpoints.

---

## 🧪 Testing

Start the test database:

```bash
docker compose up -d test_db
```

Run the complete test suite:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-fail-under=90
```

The project contains more than **200 automated tests** and maintains over **90% test coverage**.

---

## ✅ Code Quality

Check formatting with Black:

```bash
poetry run black --check .
```

Run Flake8:

```bash
poetry run flake8 .
```

Run static type checking with mypy:

```bash
poetry run mypy app
```

---

## 🚀 CI/CD

The project uses **GitHub Actions** for Continuous Integration and Continuous Deployment.

For every push and pull request, the CI pipeline automatically:

1. Checks out the repository
2. Sets up Python
3. Installs Poetry and project dependencies
4. Checks formatting with Black
5. Runs Flake8
6. Runs mypy
7. Starts the test PostgreSQL database
8. Runs the complete Pytest suite
9. Verifies that test coverage is at least 90%

After changes are pushed or merged into the `main` branch and all CI checks pass, the deployment job automatically connects to the AWS EC2 instance through SSH and deploys the latest version of the application.

### Deployment Flow

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Black + Flake8 + mypy
        ↓
Pytest + Coverage
        ↓
Push / Merge to main
        ↓
SSH Deployment
        ↓
AWS EC2
        ↓
Docker Compose
        ↓
Online Cinema API
```

---

## ☁️ AWS Deployment

The application is deployed on an **AWS EC2 Ubuntu server.**

Docker Compose manages the application services on the server.

After successful CI checks on the `main` branch, GitHub Actions connects to the EC2 instance and automatically executes the deployment process:

```bash
cd /home/ubuntu/online-cinema-project
git fetch origin
git switch main
git pull origin main
docker compose up --build -d
```

This allows new versions of the application to be automatically deployed without manually connecting to the server.

Sensitive deployment data such as the EC2 host and SSH private key are stored using **GitHub Actions Secrets** and are not committed to the repository.

---

## 📁 Project Structure

```text
online-cinema-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
├── app/
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── worker/
│   ├── __init__.py
│   └── main.py
├── scripts/
│   ├── __init__.py
│   └── seed_users.py
├── tests/
├── .env.example
├── .flake8
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

### Main Directories

- `app/core` — application configuration and core utilities
- `app/crud` — database operations
- `app/db` — database configuration and sessions
- `app/models` — SQLAlchemy database models
- `app/routers` — FastAPI API endpoints
- `app/schemas` — Pydantic request and response schemas
- `app/services` — application business logic and external service integrations
- `app/worker` — Celery background tasks and worker configuration
- `scripts` — utility scripts, including demo user seeding
- `tests` — automated test suite
- `alembic` — database migrations
- `.github/workflows` — GitHub Actions CI/CD configuration

---

## 🔐 Environment Variables

The repository contains an `.env.example` file describing the required environment variables.

Create your local configuration with:

```bash
cp .env.example .env
```

The real `.env` file is excluded from Git and should never be committed to the repository.

Environment configuration includes:

- PostgreSQL credentials
- Database URLs
- JWT configuration
- Redis connection
- Email configuration
- MinIO credentials
- Demo account credentials

Sensitive production values are stored separately and are not included in the repository.

---

## 📌 Project Status

The backend includes the main functionality of an online cinema platform together with automated testing, containerized infrastructure, background processing, object storage, and automated cloud deployment.

The project demonstrates practical experience with:

- REST API development with FastAPI
- Authentication and authorization
- JWT access and refresh tokens
- Role-based access control
- Async SQLAlchemy
- PostgreSQL database modeling
- Database migrations with Alembic
- Redis
- Celery background tasks
- S3-compatible object storage with MinIO
- Automated testing with Pytest
- Test coverage
- Static type checking with mypy
- Code formatting with Black
- Code quality checks with Flake8
- Docker and Docker Compose
- GitHub Actions CI/CD
- AWS EC2 deployment