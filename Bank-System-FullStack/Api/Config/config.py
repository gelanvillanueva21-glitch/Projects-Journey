from pydantic_settings import BaseSettings, SettingsConfigDict



# This is the settings which is connected to the
# .env file so the secret_key and database location
# con not be easily leaked
class Settings(BaseSettings):
    database_url : str = "postgresql+asyncpg://user:password@localhost/bank_db"
    secret_key : str = "duygqwdaijdjwqoifjqwo"
    algorithm : str = "HS256"
    access_token_expire_hour : int = 12
    
    model_config = SettingsConfigDict(
        env_file = "Config/.env",
        env_file_encoding = "utf-8"
    )


# Variable for the setting class
settings = Settings()


