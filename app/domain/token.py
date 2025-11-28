"""
Token domain logic for JWT authentication.

Following Domain-Driven Design principles.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from pydantic import BaseModel

from app.core.config import settings


class Token(BaseModel):
    """Token domain entity."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    refresh_token: str | None = None

    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now(UTC) >= self.expires_at

    @classmethod
    def create_access_token(
        cls, subject: str | int, expires_delta: timedelta | None = None
    ) -> str:
        """Create JWT access token."""
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # type: ignore[no-any-return]

    @classmethod
    def create_refresh_token(
        cls, subject: str | int, expires_delta: timedelta | None = None
    ) -> str:
        """Create JWT refresh token."""
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )

        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # type: ignore[no-any-return]

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        """Decode and validate JWT token."""
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # type: ignore[no-any-return]

    @classmethod
    def create_token_pair(cls, subject: str | int) -> Token:
        """Create access and refresh token pair."""
        access_token = cls.create_access_token(subject)
        refresh_token = cls.create_refresh_token(subject)

        # Calculate expiration time
        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return cls(
            access_token=access_token,
            expires_at=expires_at,
            refresh_token=refresh_token,
        )


class TokenData(BaseModel):
    """Data extracted from JWT token."""

    sub: str
    exp: datetime
    type: str
