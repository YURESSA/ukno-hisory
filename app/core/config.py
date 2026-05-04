from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    DB_BACKEND: str = "sqlite"
    SQLITE_DB_PATH: str = "./app.db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True
    LOG_INCLUDE_QUERY_STRING: bool = False
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_DEFAULT_SENDER: str
    UPLOAD_DIR: str = "uploads"
    UPLOAD_URL_PREFIX: str = "/uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @model_validator(mode="after")
    def build_database_url(self):
        if self.DATABASE_URL:
            return self

        backend = self.DB_BACKEND.lower()
        if backend == "sqlite":
            self.DATABASE_URL = f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
            return self

        if backend in {"postgres", "postgresql"}:
            self.DATABASE_URL = (
                "postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
            return self

        raise ValueError("DB_BACKEND must be either 'sqlite' or 'postgres'")

    @property
    def upload_dir_path(self) -> Path:
        return Path(self.UPLOAD_DIR)


settings = Settings()
