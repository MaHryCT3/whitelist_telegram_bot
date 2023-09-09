from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str

    BACKEND_HOST: str

    STEAM_KEY: str


settings = Settings(_env_file='.env')
