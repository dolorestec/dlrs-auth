"""
Pytest configuration for integration tests.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def patch_redis_client() -> Generator[None]:
    """Automatically patch RedisClient to avoid connection issues."""
    mock_redis = MagicMock()
    mock_redis.incr = AsyncMock(return_value=1)
    mock_redis.expire = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)

    with patch("app.infrastructure.redis_client.redis_client", mock_redis), patch(
        "app.api.v1.endpoints.auth.get_cache", return_value=mock_redis
    ):
        yield


@pytest.fixture(autouse=True)
def patch_rabbitmq_publisher() -> Generator[None]:
    """Automatically patch RabbitMQ publisher."""
    mock_publisher = MagicMock()
    mock_publisher.publish_user_logged_in = AsyncMock()
    mock_publisher.publish_token_revoked = AsyncMock()
    mock_publisher.publish_password_changed = AsyncMock()

    with patch(
        "app.infrastructure.rabbitmq_adapter.rabbitmq_publisher", mock_publisher
    ), patch(
        "app.api.v1.endpoints.auth.get_event_publisher", return_value=mock_publisher
    ):
        yield


@pytest.fixture(autouse=True)
def patch_postgres_repository() -> Generator[None]:
    """Automatically patch PostgreSQL repository."""
    mock_repo = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.is_active = True
    # Will be configured per test
    mock_user.verify_password = MagicMock(return_value=False)

    # Will be configured per test
    mock_repo.get_by_email = AsyncMock(return_value=None)

    async def mock_get_user_repository():
        return mock_repo

    with patch(
        "app.api.v1.endpoints.auth.get_user_repository",
        side_effect=mock_get_user_repository,
    ):
        yield


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

    with patch("app.infrastructure.redis_client.redis_client", mock_redis), patch(
        "app.api.v1.endpoints.auth.get_cache", return_value=mock_redis
    ):
        yield mock_redis
