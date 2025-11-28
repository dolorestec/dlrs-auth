"""
Authentication use cases.

Handles login, token validation, and refresh operations.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass
class LoginRequest:
    """Login request data."""

    email: str
    password: str


@dataclass
class TokenResponse:
    """Token response data."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginUseCase:
    """Use case for user authentication."""

    def __init__(self, user_repository: IUserRepository, cache: ICache) -> None:
        """Initialize use case with dependencies."""
        self.user_repository = user_repository
        self.cache = cache

    async def execute(self, request: LoginRequest) -> TokenResponse:
        """Execute login logic."""
        # Rate limiting check
        rate_limit_key = f"login_attempts:{request.email}"
        attempts = await self.cache.incr(rate_limit_key)
        if attempts == 1:
            # Set expiration on first attempt
            await self.cache.expire(rate_limit_key, settings.RATE_LIMIT_WINDOW_SECONDS)
        if attempts > settings.RATE_LIMIT_REQUESTS:  # Max attempts per minute
            msg = "Too many login attempts. Please try again later."
            raise ValueError(msg)

        # Get user by email
        user = await self.user_repository.get_by_email(request.email)
        if not user or not user.is_active:
            msg = "Invalid credentials"
            raise ValueError(msg)

        # Verify password
        if not user.verify_password(request.password):
            msg = "Invalid credentials"
            raise ValueError(msg)

        # Reset rate limit on successful login
        await self.cache.delete(rate_limit_key)

        # Generate JWT tokens
        if user.id is None:
            msg = "User ID is required"
            raise ValueError(msg)
        token_pair = Token.create_token_pair(user.id)

        # TODO: Publish login event to RabbitMQ

        return TokenResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token or "",
        )


class ValidateTokenUseCase:
    """Use case for token validation."""

    async def execute(self, token: str) -> dict[str, str]:  # noqa: ARG002
        """Execute token validation logic."""
        # TODO: Decode and validate JWT
        # TODO: Check if token is revoked in Redis
        # TODO: Return claims if valid

        # Placeholder response
        return {"user_id": "1", "email": "user@example.com"}


class RefreshTokenUseCase:
    """Use case for token refresh."""

    async def execute(self, refresh_token: str) -> TokenResponse:  # noqa: ARG002
        """Execute token refresh logic."""
        # TODO: Validate refresh token
        # TODO: Generate new token pair
        # TODO: Invalidate old refresh token
        # TODO: Publish refresh event

        # Placeholder response
        return TokenResponse(
            access_token="new_access_token",
            refresh_token="new_refresh_token",
        )
