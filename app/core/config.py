from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_DEFAULT_SENDER: str

    class Config:
        env_file = ".env"


settings = Settings()
