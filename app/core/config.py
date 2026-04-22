from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_DEFAULT_SENDER: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
