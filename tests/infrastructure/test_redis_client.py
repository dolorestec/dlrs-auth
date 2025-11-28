"""
Tests for Redis client infrastructure.
"""

from unittest.mock import AsyncMock, patch

import pytest

from app.infrastructure.redis_client import RedisClient

# Test constants
INCREMENT_VALUE = 5


class TestRedisClient:
    """Test RedisClient."""

    @pytest.fixture
    async def redis_client(self) -> RedisClient:
        """Redis client instance."""
        return RedisClient()

    @pytest.mark.asyncio
    async def test_connect_success(self, redis_client: RedisClient) -> None:
        """Test successful connection."""
        mock_redis = AsyncMock()

        with patch(
            "app.infrastructure.redis_client.Redis.from_url", return_value=mock_redis
        ):
            await redis_client.connect()
            assert redis_client._client is not None

    @pytest.mark.asyncio
    async def test_connect_failure(self, redis_client: RedisClient) -> None:
        """Test connection failure."""
        with (
            patch(
                "app.infrastructure.redis_client.Redis.from_url",
                side_effect=Exception("Connection failed"),
            ),
            pytest.raises(Exception, match="Connection failed"),
        ):
            await redis_client.connect()

    @pytest.mark.asyncio
    async def test_set_success(self, redis_client: RedisClient) -> None:
        """Test successful set operation."""
        mock_redis = AsyncMock()
        mock_redis.set.return_value = True

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.set("key", "value")
            assert result is True
            mock_redis.set.assert_called_once_with("key", "value", ex=None)

    @pytest.mark.asyncio
    async def test_set_with_expiry(self, redis_client: RedisClient) -> None:
        """Test set operation with expiry."""
        mock_redis = AsyncMock()
        mock_redis.set.return_value = True

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.set("key", "value", expire=300)
            assert result is True
            mock_redis.set.assert_called_once_with("key", "value", ex=300)

    @pytest.mark.asyncio
    async def test_get_success(self, redis_client: RedisClient) -> None:
        """Test successful get operation."""
        mock_redis = AsyncMock()
        mock_redis.get.return_value = "value"

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.get("key")
            assert result == "value"
            mock_redis.get.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_get_not_found(self, redis_client: RedisClient) -> None:
        """Test get operation when key not found."""
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.get("nonexistent")
            assert result is None
            mock_redis.get.assert_called_once_with("nonexistent")

    @pytest.mark.asyncio
    async def test_incr_success(self, redis_client: RedisClient) -> None:
        """Test successful incr operation."""
        mock_redis = AsyncMock()
        mock_redis.incr.return_value = INCREMENT_VALUE

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.incr("counter")
            assert result == INCREMENT_VALUE
            mock_redis.incr.assert_called_once_with("counter")

    @pytest.mark.asyncio
    async def test_expire_success(self, redis_client: RedisClient) -> None:
        """Test successful expire operation."""
        mock_redis = AsyncMock()
        mock_redis.expire.return_value = True

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.expire("key", 300)
            assert result is True
            mock_redis.expire.assert_called_once_with("key", 300)

    @pytest.mark.asyncio
    async def test_delete_success(self, redis_client: RedisClient) -> None:
        """Test successful delete operation."""
        mock_redis = AsyncMock()
        mock_redis.delete.return_value = 1

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.delete("key")
            assert result == 1
            mock_redis.delete.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_exists_success(self, redis_client: RedisClient) -> None:
        """Test successful exists operation."""
        mock_redis = AsyncMock()
        mock_redis.exists.return_value = True

        with patch.object(redis_client, "_client", mock_redis):
            result = await redis_client.exists("key")
            assert result is True
            mock_redis.exists.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_disconnect_success(self, redis_client: RedisClient) -> None:
        """Test successful disconnect operation."""
        mock_redis = AsyncMock()

        with patch.object(redis_client, "_client", mock_redis):
            await redis_client.disconnect()
            mock_redis.close.assert_called_once()
            assert redis_client._client is None
