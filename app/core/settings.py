from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAIN_DB_URL: PostgresDsn
    TENANT_DB_URL: PostgresDsn

    class Config:
        env_file = ".env"
