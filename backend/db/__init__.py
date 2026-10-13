"""
db/__init__.py
==================
Async MongoDB client using Motor.

Reads MONGODB_URI and DATABASE_NAME from environment variables (.env).
Exposes the `db` database handle and lifecycle helpers for FastAPI.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "retentio")

_client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_db() -> None:
    """Open the Motor client connection. Call once at app startup."""
    global _client, db
    if not MONGODB_URI:
        raise RuntimeError(
            "MONGODB_URI is not set. "
            "Copy .env.example → .env and fill in your MongoDB Atlas connection string."
        )
    _client = AsyncIOMotorClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10_000,  # 10-second limit instead of 30-second default
        connectTimeoutMS=10_000,
        socketTimeoutMS=20_000,
    )
    db = _client[DATABASE_NAME]
    # Verify connectivity (will raise if unreachable)
    try:
        await _client.admin.command("ping")
    except Exception as exc:
        _client.close()
        _client = None
        db = None
        raise RuntimeError(
            f"MongoDB Atlas connection failed: {exc}\n"
            "Check your MONGODB_URI, network access, and Atlas IP whitelist."
        ) from exc


async def close_db() -> None:
    """Close the Motor client. Call once at app shutdown."""
    global _client, db
    if _client is not None:
        _client.close()
        _client = None
        db = None


def get_db() -> AsyncIOMotorDatabase:
    """Return the current database handle (for use in route dependencies)."""
    if db is None:
        raise RuntimeError("Database not initialised. Call connect_db() first.")
    return db
