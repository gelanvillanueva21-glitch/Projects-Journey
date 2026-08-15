
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://taskflow:taskflow_secret@db:5432/taskflow_db"

    class Config:
        env_file = ".env"


settings = Settings()


