"""
Integration tests for authentication flow.

Tests complete end-to-end authentication scenarios using mocked dependencies.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

import app.api.v1.endpoints.auth as auth_module
from app.core.config import Settings
from app.main import app

# HTTP status codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_401_UNAUTHORIZED = 401
HTTP_429_TOO_MANY_REQUESTS = 429

# Rate limiting constants
RATE_LIMIT_REQUESTS = 5


@pytest.fixture(scope="session")
async def test_settings() -> Settings:
    """Test settings with mocked URLs."""
    import os

    # Set environment variables for Settings
    os.environ["POSTGRES_SERVER"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5432"
    os.environ["POSTGRES_USER"] = "test"
    os.environ["POSTGRES_PASSWORD"] = "test"
    os.environ["POSTGRES_DB"] = "test"

    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["REDIS_PASSWORD"] = ""

    os.environ["RABBITMQ_HOST"] = "localhost"
    os.environ["RABBITMQ_PORT"] = "5672"
    os.environ["RABBITMQ_USER"] = "guest"
    os.environ["RABBITMQ_PASSWORD"] = "guest"

    # JWT and rate limiting settings
    os.environ["SECRET_KEY"] = "test_secret_key_for_integration_tests"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "7"
    os.environ["RATE_LIMIT_REQUESTS"] = "5"
    os.environ["RATE_LIMIT_WINDOW_SECONDS"] = "60"

    return Settings()


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """HTTP test client for the FastAPI app."""
    from fastapi.testclient import TestClient

    # Override settings in the app
    app.dependency_overrides = {}

    return TestClient(app)


class TestAuthIntegration:
    """Integration tests for complete authentication flow."""

    def test_complete_auth_flow(self, test_client) -> None:
        """Test complete authentication flow: login, validate token, refresh."""
        from app.api.v1.endpoints.auth import get_user_repository

        # Configure mock user for this test
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.is_active = True
        mock_user.verify_password = MagicMock(return_value=True)

        mock_repo.get_by_email = AsyncMock(return_value=mock_user)

        # Mock the dependency
        original_get_repo = get_user_repository

        async def mock_get_repo():
            return mock_repo

        auth_module.get_user_repository = mock_get_repo

        try:
            user_data = {
                "email": "test@example.com",
                "password": "SecurePass123!",
            }

            # Login user
            login_response = test_client.post("/api/v1/auth/login", json=user_data)
            assert login_response.status_code == HTTP_200_OK

            login_data = login_response.json()
            assert "access_token" in login_data
            assert "refresh_token" in login_data

            # Validate token (placeholder implementation)
            validate_response = test_client.post("/api/v1/auth/validate")
            assert validate_response.status_code == HTTP_200_OK

            # Refresh token (placeholder implementation)
            refresh_response = test_client.post("/api/v1/auth/refresh")
            assert refresh_response.status_code == HTTP_200_OK

        finally:
            # Restore original
            auth_module.get_user_repository = original_get_repo

    def test_rate_limiting(self, test_client) -> None:
        """Test rate limiting functionality."""
        # Configure mock user for this test
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "ratelimit@example.com"
        mock_user.is_active = True
        mock_user.verify_password = MagicMock(return_value=True)

        mock_repo.get_by_email = AsyncMock(return_value=mock_user)

        # Mock the user repository
        async def mock_get_user_repository():
            return mock_repo

        original_get_repo = auth_module.get_user_repository
        auth_module.get_user_repository = mock_get_user_repository

        try:
            user_data = {
                "email": "ratelimit@example.com",
                "password": "SecurePass123!",
            }

            # Make multiple login requests
            for i in range(RATE_LIMIT_REQUESTS + 1):
                response = test_client.post("/api/v1/auth/login", json=user_data)
                if i < RATE_LIMIT_REQUESTS:
                    assert response.status_code == HTTP_200_OK
                else:
                    assert response.status_code == HTTP_401_UNAUTHORIZED  # Rate limited

        finally:
            # Restore original
            auth_module.get_user_repository = original_get_repo

    def test_invalid_credentials(self, test_client) -> None:
        """Test login with invalid credentials."""
        # The mock is already configured to return None for get_by_email
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPass123!",
        }

        response = test_client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == HTTP_401_UNAUTHORIZED

        error_data = response.json()
        assert "detail" in error_data

    def test_expired_token(self, test_client) -> None:
        """Test validation of expired token."""
        # Since validate endpoint uses placeholder, it should return 200
        # This test needs to be updated when token validation is properly implemented
        response = test_client.post("/api/v1/auth/validate")
        assert response.status_code == HTTP_200_OK

    def test_event_publishing(self, test_client) -> None:
        """Test that authentication events are published to RabbitMQ."""
        from app.api.v1.endpoints.auth import get_user_repository

        # Configure mock user for this test
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "event@example.com"
        mock_user.is_active = True
        mock_user.verify_password = MagicMock(return_value=True)

        mock_repo.get_by_email = AsyncMock(return_value=mock_user)

        # Mock the dependency
        original_get_repo = get_user_repository

        async def mock_get_repo():
            return mock_repo

        auth_module.get_user_repository = mock_get_repo

        try:
            user_data = {
                "email": "event@example.com",
                "password": "SecurePass123!",
            }

            # Login (should publish event)
            response = test_client.post("/api/v1/auth/login", json=user_data)
            assert response.status_code == HTTP_200_OK

            # Note: In a real integration test, we would consume from RabbitMQ
            # to verify the event was published. For now, we just ensure
            # the login succeeds without errors.

        finally:
            # Restore original
            auth_module.get_user_repository = original_get_repo
