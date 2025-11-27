"""
Redis client adapter for caching and rate limiting.

Following Clean Architecture principles.
"""

from __future__ import annotations

import json
from typing import Any

import aioredis

from app.core.config import settings
from app.infrastructure.interfaces import ICache


class RedisClient(ICache):
    """Redis client adapter."""

    def __init__(self) -> None:
        self._client: aioredis.Redis | None = None

    async def connect(self) -> None:
        """Connect to Redis."""
        if not self._client:
            self._client = aioredis.from_url(settings.redis_url)

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> str | None:
        """Get value from Redis."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.get(key)

    async def set(self, key: str, value: str, expire: int | None = None) -> bool:
        """Set value in Redis with optional expiration."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> int:
        """Delete key from Redis."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.exists(key)

    async def incr(self, key: str) -> int:
        """Increment integer value in Redis."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.incr(key)

    async def expire(self, key: str, time: int) -> bool:
        """Set expiration time for key."""
        if not self._client:
            await self.connect()
        assert self._client is not None
        return await self._client.expire(key, time)

    async def get_json(self, key: str) -> Any | None:
        """Get JSON value from Redis."""
        value = await self.get(key)
        return json.loads(value) if value else None

    async def set_json(self, key: str, value: Any, expire: int | None = None) -> bool:
        """Set JSON value in Redis."""
        json_value = json.dumps(value)
        return await self.set(key, json_value, expire)


# Global instance
redis_client = RedisClient()
