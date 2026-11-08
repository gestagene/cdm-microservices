from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    port: int = 8001            # default if .env doesn't set it
    database_url: str = ""

settings = Settings()