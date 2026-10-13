from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

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
    MAIL_PASSWORD: str = ""
    MAIL_SERVER: str = "localhost"
    MAIL_PORT: int = 1025
    MAIL_USERNAME: str = ""
    MAIL_DEFAULT_SENDER: str = "no-reply@example.com"
    SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GRAFANA_SESSION_EXPIRE_MINUTES: int = 480
    UPLOAD_DIR: str = str(BACKEND_DIR / "uploads")
    UPLOAD_URL_PREFIX: str = "/uploads"
    STORAGE_BACKEND: str = "local"
    S3_ENDPOINT: str = "https://s3.twcstorage.ru"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = ""
    S3_REGION: str = "ru-1"
    S3_ADDRESSING_STYLE: str = "path"
    S3_KEY_PREFIX: str = "5history"
    S3_PRESIGNED_URL_EXPIRES: int = 3600

    model_config = SettingsConfigDict(
        env_file=(
            PROJECT_ROOT / ".env",
            BACKEND_DIR / ".env",
        ),
        extra="ignore",
    )

    @model_validator(mode="after")
    def build_database_url(self):
        if self.STORAGE_BACKEND not in {"local", "s3"}:
            raise ValueError("STORAGE_BACKEND must be 'local' or 's3'")
        if self.STORAGE_BACKEND == "s3" and not all(
            (
                self.S3_ENDPOINT,
                self.S3_ACCESS_KEY,
                self.S3_SECRET_KEY,
                self.S3_BUCKET,
                self.S3_KEY_PREFIX.strip("/"),
            )
        ):
            raise ValueError(
                "S3 endpoint, credentials, bucket and key prefix are required"
            )
        if self.DATABASE_URL:
            return self

        backend = self.DB_BACKEND.lower()
        if backend == "sqlite":
            sqlite_path = _resolve_project_path(self.SQLITE_DB_PATH)
            self.SQLITE_DB_PATH = str(sqlite_path)
            self.DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"
            return self

        if backend in {"postgres", "postgresql"}:
            self.DATABASE_URL = URL.create(
                "postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                database=self.POSTGRES_DB,
            ).render_as_string(hide_password=False)
            return self

        raise ValueError("DB_BACKEND must be either 'sqlite' or 'postgres'")

    @property
    def upload_dir_path(self) -> Path:
        return _resolve_project_path(self.UPLOAD_DIR)


settings = Settings()
