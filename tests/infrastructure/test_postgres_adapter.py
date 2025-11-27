"""
Tests for PostgreSQL adapter.
"""

from types import TracebackType
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from faker import Faker

from app.infrastructure.postgres_adapter import PostgresUserRepository


class AsyncContextManagerMock:
    """Mock for async context manager."""

    def __init__(self, conn: Any) -> None:
        self.conn = conn

    async def __aenter__(self) -> Any:
        return self.conn

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass


@pytest.fixture
async def repo() -> PostgresUserRepository:
    """Create repository instance."""
    return PostgresUserRepository()


@pytest.fixture
def faker() -> Faker:
    """Create Faker instance for test data generation."""
    return Faker()


@pytest.mark.asyncio
async def test_get_by_email_found(repo: PostgresUserRepository, faker: Faker) -> None:
    """Test retrieving existing user by email."""
    fake_email = faker.email()
    fake_id = faker.random_int(min=1, max=1000)

    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": fake_id,
        "email": fake_email,
        "hashed_password": faker.password(),
        "is_active": faker.boolean(),
        "created_at": faker.date_time().isoformat(),
        "updated_at": faker.date_time().isoformat(),
    }

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.get_by_email(fake_email)
        assert result is not None
        assert result.email == fake_email
        assert result.id == fake_id


@pytest.mark.asyncio
async def test_get_by_email_not_found(
    repo: PostgresUserRepository, faker: Faker
) -> None:
    """Test retrieving non-existent user by email."""
    fake_email = faker.email()

    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.get_by_email(fake_email)
        assert result is None
