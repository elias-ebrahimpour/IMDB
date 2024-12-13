from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "127.0.0.1:8000"
    port: int = 8000
    mongodb_url: str = "mongodb://localhost:27017/"
    imdb_api_key: str = "xxxxxx"
    telegram_bot: str = "xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxx"

    model_config = SettingsConfigDict(env_file=".env")
