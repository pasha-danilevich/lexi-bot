from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(BASE_PATH, "dev.env"),
        env_file_encoding="utf-8",
        # env_ignore_empty=True,
        extra="ignore",
    )


class Bot(Base):
    BOT_TOKEN: str


class Postgres(Base):
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 15432
    DB_NAME: str = "dbname"


class Config(Bot, Postgres):
    pass


@lru_cache()
def get_config() -> Config:
    return Config()


config: Config = get_config()
