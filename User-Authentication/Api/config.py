from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url : str = "postgre+asyncpg://user:password@localhost/users"
    secret_key : str = "temporary_string"
    algorithm : str = "HS256"
    access_token_expr : int = 30
    
    class Config:
        env_file = ".env"


setting = Settings()