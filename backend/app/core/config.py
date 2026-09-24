from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgentScout"
    DEBUG: bool = True

    # ── Database ─────────────────────────────────────────────
    # For Supabase: use the connection-pooler URL (port 6543)
    # Format: postgresql+asyncpg://<user>:<password>@<host>:6543/postgres
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/agentscout"

    # Optional: Supabase project keys (only needed if you later
    # call Supabase REST/Auth directly from the backend)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # LLM (Gemini)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # JWT Auth
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Firecrawl
    FIRECRAWL_API_KEY: str = ""

    # Web search provider (for company-name lookup)
    TAVILY_API_KEY: str = ""
    TAVILY_BASE_URL: str = "https://api.tavily.com"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
