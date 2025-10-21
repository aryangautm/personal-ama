from .base_config import BaseConfig


class Settings(BaseConfig):

    CORS_ORIGINS: str
    APP_AUTH_KEY: str

    GEMINI_API_KEY: str
    GEMINI_CHAT_LLM: str = "gemini-2.5-flash"


settings = Settings()
