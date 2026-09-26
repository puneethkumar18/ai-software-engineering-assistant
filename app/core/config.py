from pydantic_settings import BaseSettings,SettingsConfigDict 


class Settings(BaseSettings):
    APP_NAME: str = "AI Software Engineering Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool 

    GEMINI_API_KEY: str

    DATABASE_URL: str

    AGENT_MAX_ITERATIONS: int = 5
    AGENT_MAX_TOOL_CALLS: int = 10

    LLM_TIMEOUT_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()