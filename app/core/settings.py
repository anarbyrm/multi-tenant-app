from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    MAIN_DB_NAME: str
    TENANT_DB_NAME: str
    MAIN_DB_URL: str
    TENANT_DB_URL: str
    ACCESS_TOKEN_EXPIRE: int
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
