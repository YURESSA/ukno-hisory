from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


def _resolve_project_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    DB_BACKEND: str = "sqlite"
    SQLITE_DB_PATH: str = str(BACKEND_DIR / "data" / "app.db")
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True
    LOG_INCLUDE_QUERY_STRING: bool = False
    LOG_SQL_QUERIES: bool = False
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_DEFAULT_SENDER: str
    SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GRAFANA_SESSION_EXPIRE_MINUTES: int = 480
    UPLOAD_DIR: str = str(BACKEND_DIR / "uploads")
    UPLOAD_URL_PREFIX: str = "/uploads"

    model_config = SettingsConfigDict(
        env_file=(
            PROJECT_ROOT / ".env",
            BACKEND_DIR / ".env",
        ),
        extra="ignore",
    )

    @model_validator(mode="after")
    def build_database_url(self):
        if self.DATABASE_URL:
            return self

        backend = self.DB_BACKEND.lower()
        if backend == "sqlite":
            sqlite_path = _resolve_project_path(self.SQLITE_DB_PATH)
            self.SQLITE_DB_PATH = str(sqlite_path)
            self.DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"
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
        return _resolve_project_path(self.UPLOAD_DIR)


settings = Settings()
