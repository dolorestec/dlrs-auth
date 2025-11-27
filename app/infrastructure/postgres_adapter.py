"""
PostgreSQL adapter for user repository operations.

Implements IUserRepository using asyncpg for database operations.
Provides connection pooling and error handling for user CRUD operations.
"""

from __future__ import annotations

import asyncpg
import structlog

from app.core.config import settings
from app.domain.user import User
from app.infrastructure.interfaces import IUserRepository

logger = structlog.get_logger()


class PostgresUserRepository(IUserRepository):
    """PostgreSQL implementation of user repository."""

    def __init__(self) -> None:
        """Initialize repository with connection pool."""
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        """Get or create database connection pool."""
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                settings.sqlalchemy_database_uri,
                min_size=5,
                max_size=20,
                command_timeout=60,
            )
        return self._pool

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email address."""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT id, email, hashed_password, is_active, "
                    "created_at, updated_at FROM users WHERE email = $1",
                    email,
                )
                return User(**row) if row else None
        except asyncpg.exceptions.PostgresError:
            logger.exception("Database error in get_by_email")
            raise
