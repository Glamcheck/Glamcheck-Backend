from typing import Annotated

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

SecretKey = Annotated[str, Field(min_length=64)]


class Settings(BaseSettings):
    db_connection_string: str

    access_token_secret_key: SecretKey
    access_token_expire_minutes: PositiveInt
    access_token_algorithm: str

    refresh_token_secret_key: SecretKey
    refresh_token_expire_days: PositiveInt
    refresh_token_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
