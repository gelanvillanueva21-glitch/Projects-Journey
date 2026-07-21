from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url : str = "postgresql+asyncpg://user:password@localhost/url_shortener"
    secret_key : str = "fhasoewiqfaw"
    algorithm : str = "HelloWorld"
    access_token_expire_minutes : int = 30
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8")



settings = Settings()