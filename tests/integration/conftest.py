"""
Pytest configuration for integration tests.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_redis_client() -> Generator[MagicMock]:
    """Fixture for Redis client with default behavior (incr returns 1)."""
    mock_redis = MagicMock()
    mock_redis.incr = AsyncMock(return_value=1)
    mock_redis.expire = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)

    with (
        patch("app.infrastructure.redis_client.redis_client", mock_redis),
        patch("app.api.v1.endpoints.auth.get_cache", return_value=mock_redis),
    ):
        yield mock_redis


@pytest.fixture
def patch_redis_client(mock_redis_client) -> Generator[None]:
    """Patch RedisClient for tests that need default behavior."""
    return


@pytest.fixture
def mock_rate_limiting_redis() -> Generator[MagicMock]:
    """Fixture for rate limiting test with increasing incr values."""
    call_count = 0

    async def mock_incr(_key: str) -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    mock_redis = MagicMock()
    mock_redis.incr = mock_incr
    mock_redis.expire = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)

    with (
        patch("app.infrastructure.redis_client.redis_client", mock_redis),
        patch("app.api.v1.endpoints.auth.get_cache", return_value=mock_redis),
    ):
        yield mock_redis


@pytest.fixture
def mock_rabbitmq_publisher() -> Generator[MagicMock]:
    """Fixture for RabbitMQ event publisher."""
    mock_publisher = MagicMock()
    mock_publisher.publish_user_logged_in = AsyncMock()
    mock_publisher.publish_token_revoked = AsyncMock()
    mock_publisher.publish_password_changed = AsyncMock()
    mock_publisher.connect = AsyncMock()
    mock_publisher.disconnect = AsyncMock()

    with patch(
        "app.api.v1.endpoints.auth.get_event_publisher", return_value=mock_publisher
    ):
        yield mock_publisher


@pytest.fixture
def mock_postgres_repository() -> Generator[MagicMock]:
    """Fixture for PostgreSQL user repository."""
    mock_repo = MagicMock()
    mock_repo.get_by_email = AsyncMock(
        return_value=None
    )  # Default to None (user not found)

    with patch("app.api.v1.endpoints.auth.get_user_repository", return_value=mock_repo):
        yield mock_repo


@pytest.fixture(autouse=True)
def patch_dependencies(
    mock_rabbitmq_publisher, mock_postgres_repository
) -> Generator[None]:
    """Automatically patch RabbitMQ and PostgreSQL dependencies."""
    return


@pytest.fixture(autouse=True)
def patch_redis_default(mock_redis_client) -> Generator[None]:
    """Automatically patch Redis with default behavior."""
    return
