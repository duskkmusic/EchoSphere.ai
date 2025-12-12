from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Debate System"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # Database
    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    # Redis
    REDIS_URL: str

    # Celery
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Groq — LIDA DIRETAMENTE DO OS, IGNORA .env
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Rate limit
    RATE_LIMIT_FREE_TIER: int = 10
    RATE_LIMIT_PREMIUM_TIER: int = 50
    RATE_LIMIT_ADMIN_TIER: int = 1000

    # Documents
    MAX_DOCUMENT_SIZE_MB: int = 10
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Agents
    MAX_CONCURRENT_AGENTS: int = 5
    AGENT_TIMEOUT_SECONDS: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
