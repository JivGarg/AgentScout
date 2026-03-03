"""
AgentScout Backend – FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.api.auth import router as auth_router
from app.api.research import router as research_router
from app.api.resume import router as resume_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
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
