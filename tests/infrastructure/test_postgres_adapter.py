from unittest.mock import AsyncMock

import pytest

from app.domain.user import UserCreate
from app.infrastructure.postgres_adapter import PostgresUserRepository


@pytest.fixture
async def repo():
    repo = PostgresUserRepository()
    # Mock the pool for testing
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    mock_pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_pool.acquire.return_value.__aexit__ = AsyncMock()
    repo._pool = mock_pool
    return repo


@pytest.mark.asyncio
async def test_get_by_email_found(repo):
    mock_conn = repo._pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "test@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
    }

    result = await repo.get_by_email("test@example.com")
    assert result is not None
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_by_email_not_found(repo):
    mock_conn = repo._pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.return_value = None

    result = await repo.get_by_email("notfound@example.com")
    assert result is None


@pytest.mark.asyncio
async def test_create_user(repo):
    mock_conn = repo._pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "new@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
    }

    user_create = UserCreate(email="new@example.com", password="password")
    result = await repo.create_user(user_create)
    assert result.id == 1
    assert result.email == "new@example.com"
