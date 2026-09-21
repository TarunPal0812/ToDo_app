import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv("APP_NAME","development")

class Settings(BaseSettings):

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=f".env.{env_state}",
        extra= "ignore"
        )


setting = Settings() # type: ignore