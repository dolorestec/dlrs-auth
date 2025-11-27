"""
PostgreSQL adapter for user repository operations.

Implements IUserRepository using asyncpg for database operations.
Provides connection pooling and error handling for user CRUD operations.
"""

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

    async def create_user(self, user: UserCreate) -> User:
        """Create a new user in database."""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    INSERT INTO users (email, hashed_password, is_active,
                                       created_at, updated_at)
                    VALUES ($1, $2, $3, NOW(), NOW())
                    RETURNING id, email, hashed_password, is_active,
                              created_at, updated_at
                    """,
                    user.email,
                    user.password,
                    True,
                )
                return User(**row)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.exception("User with email already exists", email=user.email)
            msg = "User already exists"
            raise ValueError(msg) from e
        except asyncpg.exceptions.PostgresError:
            logger.exception("Database error in create_user")
            raise

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        """Update user information by ID."""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                # Build dynamic update query
                update_fields = []
                values = []
                if user_update.email is not None:
                    update_fields.append("email = $" + str(len(values) + 1))
                    values.append(user_update.email)
                if user_update.is_active is not None:
                    update_fields.append("is_active = $" + str(len(values) + 1))
                    values.append(user_update.is_active)

                if not update_fields:
                    # Get user by ID instead of email
                    row = await conn.fetchrow(
                        "SELECT id, email, hashed_password, is_active, "
                        "created_at, updated_at FROM users WHERE id = $1",
                        user_id,
                    )
                    return User(**row) if row else None

                values.append(user_id)
                query = f"""
                    UPDATE users SET {', '.join(update_fields)}, updated_at = NOW()
                    WHERE id = ${len(values)}
                    RETURNING id, email, hashed_password, is_active,
                              created_at, updated_at
                """

                row = await conn.fetchrow(query, *values)
                return User(**row) if row else None
        except asyncpg.exceptions.PostgresError:
            logger.exception("Database error in update_user")
            raise

    async def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                result = await conn.execute("DELETE FROM users WHERE id = $1", user_id)
                return result == "DELETE 1"
        except asyncpg.exceptions.PostgresError:
            logger.exception("Database error in delete_user")
            raise
