from .base_config import BaseConfig


class Settings(BaseConfig):

    CORS_ORIGINS: str
    APP_AUTH_KEY: str

    GOOGLE_API_KEY: str
    GEMINI_CHAT_LLM: str = "gemini-2.5-flash"

    RATE_LIMIT: str = "50/minute"


settings = Settings()
