from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url : str = "postgresql+asyncpg://user:password@localhost/bank_db"
    secret_key : str = "duygqwdaijdjwqoifjqwo"
    algorithm : str = "HS256"
    access_token_expire_hour : int = 12
    
    model_config = SettingsConfigDict(
        env_file = "Config/.env",
        env_file_encoding = "utf-8"
    )



settings = Settings()


