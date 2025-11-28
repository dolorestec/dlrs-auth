"""
Interfaces for infrastructure adapters.

Following SOLID principles, specifically Interface Segregation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.domain.user import User


class ICache(ABC):
    """Interface for cache operations."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Get value from cache."""

    @abstractmethod
    async def set(self, key: str, value: str, expire: int | None = None) -> bool:
        """Set value in cache with optional expiration."""

    @abstractmethod
    async def delete(self, key: str) -> int:
        """Delete key from cache."""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""

    @abstractmethod
    async def incr(self, key: str) -> int:
        """Increment integer value in cache."""

    @abstractmethod
    async def expire(self, key: str, time: int) -> bool:
        """Set expiration time for key."""

    @abstractmethod
    async def get_json(self, key: str) -> Any | None:
        """Get JSON value from cache."""

    @abstractmethod
    async def set_json(self, key: str, value: Any, expire: int | None = None) -> bool:
        """Set JSON value in cache."""


class IUserRepository(ABC):
    """Interface for user repository operations."""

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email address."""


class IEventPublisher(ABC):
    """Interface for event publishing operations."""

    @abstractmethod
    async def publish_user_logged_in(
        self, user_id: int, email: str, ip_address: str | None = None
    ) -> None:
        """Publish user login event."""

    @abstractmethod
    async def publish_token_revoked(self, user_id: int, token_type: str) -> None:
        """Publish token revocation event."""

    @abstractmethod
    async def publish_password_changed(self, user_id: int) -> None:
        """Publish password change event."""

    @abstractmethod
    async def connect(self) -> None:
        """Connect to message broker."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from message broker."""
