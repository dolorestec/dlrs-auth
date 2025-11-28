"""
Pytest configuration and global fixtures.
"""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from faker import Faker


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker instance for generating test data."""
    return Faker("pt_BR")


@pytest.fixture
def mock_settings() -> MagicMock:
    """Mock settings for tests."""
    settings = MagicMock()
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
    settings.REFRESH_TOKEN_EXPIRE_DAYS = 7
    settings.SECRET_KEY = "test_secret_key_for_jwt_tokens"
    settings.ALGORITHM = "HS256"
    settings.RATE_LIMIT_REQUESTS = 5
    settings.RATE_LIMIT_WINDOW_SECONDS = 300
    return settings


@pytest.fixture
def fake_email(faker: Faker) -> str:
    """Generate a fake email."""
    return faker.email()


@pytest.fixture
def fake_password() -> str:
    """Generate a fake password."""
    return "TestPass123!"


@pytest.fixture
def fake_user_id(faker: Faker) -> int:
    """Generate a fake user ID."""
    return faker.random_int(min=1, max=10000)


@pytest.fixture
def fake_subject(faker: Faker) -> str:
    """Generate a fake JWT subject."""
    return str(faker.random_int(min=1, max=10000))


@pytest.fixture
def fake_short_password() -> str:
    """Generate a short password for validation tests."""
    return "short"


@pytest.fixture
def fake_invalid_email() -> str:
    """Generate an invalid email for validation tests."""
    return "invalid-email"


@pytest.fixture
def mock_pwd_context_hash() -> MagicMock:
    """Mock pwd_context.hash for password hashing tests."""
    mock_hash = MagicMock()
    mock_hash.return_value = (
        "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMJyHnUeK"
    )
    return mock_hash


@pytest.fixture
def mock_pwd_context_verify() -> MagicMock:
    """Mock pwd_context.verify for password verification tests."""
    mock_verify = MagicMock()
    mock_verify.return_value = True  # Default to True for successful verification
    return mock_verify


@pytest.fixture(autouse=True)
def patch_pwd_context(
    mock_pwd_context_hash: MagicMock, mock_pwd_context_verify: MagicMock
) -> Generator[None]:
    """Automatically patch pwd_context.hash and pwd_context.verify in all tests."""
    with (
        patch("app.domain.user.pwd_context.hash", mock_pwd_context_hash),
        patch("app.domain.user.pwd_context.verify", mock_pwd_context_verify),
    ):
        yield


@pytest.fixture(autouse=True)
def patch_redis_client() -> Generator[None]:
    """Automatically patch redis_client to avoid redis[asyncio] import issues."""
    mock_redis = MagicMock()
    with patch("app.infrastructure.redis_client.redis_client", mock_redis):
        yield
