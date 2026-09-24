"""
AgentScout Backend – FastAPI Application Entry Point
"""

import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Windows consoles default to a legacy codepage (e.g. cp1252) that can't
# encode emoji/en-dash characters used in log messages below, which crashes
# the app on startup. Force UTF-8 stdout/stderr so logging is safe on every OS.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

from app.core.config import get_settings
from app.core.database import init_db
from app.api.auth import router as auth_router
from app.api.research import router as research_router
from app.api.resume import router as resume_router

settings = get_settings()


DEFAULT_SECRET_KEY = "your-super-secret-key-change-in-production"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    if settings.SECRET_KEY == DEFAULT_SECRET_KEY:
        print(
            "⚠️  SECURITY WARNING: SECRET_KEY is still the default placeholder. "
            "Set a random SECRET_KEY in backend/.env before deploying."
        )
    if not (settings.GEMINI_API_KEY or "").strip():
        print("⚠️  GEMINI_API_KEY is not set — research/resume analysis will fail until it is.")

    # Startup: create tables
    await init_db()
    print(f"🚀 {settings.APP_NAME} backend started!")
    yield
    # Shutdown
    print(f"👋 {settings.APP_NAME} backend shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Deep-Research Outreach Agent – AI-powered B2B sales research",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(resume_router, prefix="/api")


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}
