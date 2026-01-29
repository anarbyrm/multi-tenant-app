from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAIN_DB_URL: PostgresDsn
    TENANT_DB_URL: PostgresDsn
    ACCESS_TOKEN_EXPIRE: int
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
