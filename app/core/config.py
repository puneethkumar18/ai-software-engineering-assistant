from pydantic_settings import BaseSettings,SettingsConfigDict 


class Settings(BaseSettings):
    APP_NAME: str = "AI Software Engineering Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    GEMINI_API_KEY: str

    DATABASE_URL: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()