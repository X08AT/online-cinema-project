from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    REDIS_URL: str

    MAIL_HOST: str
    MAIL_PORT: int
    MAIL_FROM: str

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str
    MINIO_BUCKET: str

    DEFAULT_USER_EMAIL: str
    DEFAULT_USER_PASSWORD: str

    DEFAULT_MODERATOR_EMAIL: str
    DEFAULT_MODERATOR_PASSWORD: str

    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
