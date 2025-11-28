from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.domain.user import UserCreate, UserUpdate
from app.infrastructure.postgres_adapter import PostgresUserRepository


class AsyncContextManagerMock:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def test_password() -> str:
    return "secure_test_password_not_for_production"


@pytest.fixture
async def repo():
    return PostgresUserRepository()


@pytest.mark.asyncio
async def test_get_by_email_found(repo: PostgresUserRepository) -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "test@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
    }

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.get_by_email("test@example.com")
        assert result is not None
        assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_by_email_not_found(repo: PostgresUserRepository) -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.get_by_email("notfound@example.com")
        assert result is None


@pytest.mark.asyncio
async def test_create_user(repo: PostgresUserRepository) -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "new@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
    }

    user_create = UserCreate(email="new@example.com", password="test_password_123")

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.create_user(user_create)
        assert result.id == 1
        assert result.email == "new@example.com"


@pytest.mark.asyncio
async def test_update_user_email(repo: PostgresUserRepository) -> None:
    """Test updating user email."""
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "updated@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-02",
    }

    user_update = UserUpdate(email="updated@example.com")

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.update_user(1, user_update)
        assert result is not None
        assert result.email == "updated@example.com"


@pytest.mark.asyncio
async def test_update_user_is_active(repo: PostgresUserRepository) -> None:
    """Test updating user active status."""
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "test@example.com",
        "hashed_password": "hash",
        "is_active": False,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-02",
    }

    user_update = UserUpdate(is_active=False)

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.update_user(1, user_update)
        assert result is not None
        assert result.is_active is False


@pytest.mark.asyncio
async def test_update_user_no_changes(repo: PostgresUserRepository) -> None:
    """Test updating user with no changes."""
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "email": "test@example.com",
        "hashed_password": "hash",
        "is_active": True,
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
    }

    user_update = UserUpdate()

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.update_user(1, user_update)
        assert result is not None
        assert result.id == 1


@pytest.mark.asyncio
async def test_update_user_not_found(repo: PostgresUserRepository) -> None:
    """Test updating non-existent user."""
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    user_update = UserUpdate(email="new@example.com")

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.update_user(999, user_update)
        assert result is None


@pytest.mark.asyncio
async def test_delete_user_success(repo: PostgresUserRepository) -> None:
    """Test successful user deletion."""
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = "DELETE 1"

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.delete_user(1)
        assert result is True


@pytest.mark.asyncio
async def test_delete_user_not_found(repo: PostgresUserRepository) -> None:
    """Test deleting non-existent user."""
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = "DELETE 0"

    mock_pool = MagicMock()
    mock_pool.acquire.return_value = AsyncContextManagerMock(mock_conn)

    with patch.object(repo, "_get_pool", return_value=mock_pool):
        result = await repo.delete_user(999)
        assert result is False
