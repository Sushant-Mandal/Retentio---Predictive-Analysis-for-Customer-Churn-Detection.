"""
main.py
=======
FastAPI application entry point for Retentio backend.

- Configures CORS middleware
- Connects to MongoDB on startup
- Loads ML model artifacts on startup
- Mounts all API route modules under /api/v1
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle events."""
    # ── Startup ─────────────────────────────────────────────────────────
    # 1. Connect to MongoDB
    from db import connect_db
    await connect_db()

    # 2. Load ML model into memory
    from services.ml_service import load_model
    load_model()

    yield

    # ── Shutdown ────────────────────────────────────────────────────────
    from db import close_db
    await close_db()


app = FastAPI(
    title="Retentio API",
    description="Customer churn prediction platform — backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────────────────

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount route modules ────────────────────────────────────────────────────

from api.routes.auth import router as auth_router
from api.routes.customers import router as customers_router
from api.routes.dashboard import router as dashboard_router
from api.routes.predict import router as predict_router
from api.routes.settings import router as settings_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")


@app.get("/api/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "retentio-api"}
