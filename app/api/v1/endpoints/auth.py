"""
Authentication API endpoints.

Provides login, token validation, and refresh endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.infrastructure.postgres_adapter import PostgresUserRepository
from app.infrastructure.rabbitmq_adapter import (
    RabbitMQEventPublisher,
    rabbitmq_publisher,
)
from app.infrastructure.redis_client import RedisClient, redis_client
from app.use_cases.auth import (
    LoginRequest,
    LoginUseCase,
    RefreshTokenUseCase,
    TokenResponse,
    ValidateTokenUseCase,
)

# TODO: Remove these placeholders when implementing real token extraction from requests
# Temporary constants until proper token extraction from Authorization headers
# is implemented
PLACEHOLDER_TOKEN = "placeholder_token"  # nosec B105
PLACEHOLDER_REFRESH_TOKEN = "placeholder_refresh_token"  # nosec B105

router = APIRouter()
security = HTTPBearer()


async def get_user_repository() -> PostgresUserRepository:
    """Dependency to get user repository."""
    return PostgresUserRepository()


async def get_cache() -> RedisClient:
    """Dependency to get cache client."""
    return redis_client


async def get_event_publisher() -> RabbitMQEventPublisher:
    """Dependency to get event publisher."""
    return rabbitmq_publisher


async def get_login_use_case() -> LoginUseCase:
    """Dependency to get login use case."""
    repo = await get_user_repository()
    cache = await get_cache()
    event_publisher = await get_event_publisher()
    return LoginUseCase(repo, cache, event_publisher)


async def get_validate_use_case() -> ValidateTokenUseCase:
    """Dependency to get validate token use case."""
    return ValidateTokenUseCase()


async def get_refresh_use_case() -> RefreshTokenUseCase:
    """Dependency to get refresh token use case."""
    return RefreshTokenUseCase()


@router.post("/login", response_model=TokenResponse)  # type: ignore[misc]
async def login(
    request: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> TokenResponse:
    """
    Authenticate user and return JWT tokens.

    - **email**: User email address
    - **password**: User password
    """
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.post("/validate")  # type: ignore[misc]
async def validate_token(
    use_case: ValidateTokenUseCase = Depends(get_validate_use_case),
) -> dict[str, str]:
    """
    Validate JWT token and return claims.

    Requires Bearer token in Authorization header.
    """
    # TODO: Extract token from request
    token = PLACEHOLDER_TOKEN
    try:
        return await use_case.execute(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.post("/refresh", response_model=TokenResponse)  # type: ignore[misc]
async def refresh_token(
    use_case: RefreshTokenUseCase = Depends(get_refresh_use_case),
) -> TokenResponse:
    """
    Refresh access token using refresh token.

    Requires refresh token in request body.
    """
    # TODO: Extract refresh token from request
    refresh_token = PLACEHOLDER_REFRESH_TOKEN
    try:
        return await use_case.execute(refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
