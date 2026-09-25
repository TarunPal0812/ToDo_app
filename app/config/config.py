import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv("APP_ENV","development")

class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_ACCESS_TOKEN_SECRET: str
    JWT_REFRESH_TOKEN_SECRET: str

    model_config = SettingsConfigDict(
        env_file=f".env.{env_state}",
        extra= "ignore"
        )


setting = Settings() # type: ignore