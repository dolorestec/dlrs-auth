"""
Tests for domain entities.
"""

from datetime import UTC, datetime

import pytest
from faker import Faker

from app.domain.user import User, UserCreate, UserUpdate


@pytest.fixture
def faker() -> Faker:
    """Create Faker instance for test data generation."""
    return Faker()


@pytest.fixture
def test_hashed_password(faker: Faker) -> str:
    """Generate a test hashed password."""
    return faker.password()


@pytest.fixture
def test_email(faker: Faker) -> str:
    """Generate a test email."""
    return faker.email()


@pytest.fixture
def test_password(faker: Faker) -> str:
    """Generate a test password."""
    return faker.password(length=12)


@pytest.fixture
def short_password() -> str:
    """Generate a short password for validation tests."""
    return "short"


class TestUser:
    """Test User domain entity."""

    def test_user_creation(self, test_email: str, test_hashed_password: str) -> None:
        """Test creating a user with all fields."""
        user = User(
            id=1,
            email=test_email,
            hashed_password=test_hashed_password,
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=UTC),
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        assert user.id == 1
        assert user.email == test_email
        assert user.hashed_password == test_hashed_password
        assert user.is_active is True

    def test_user_creation_defaults(
        self, test_email: str, test_hashed_password: str
    ) -> None:
        """Test creating a user with default values."""
        user = User(
            email=test_email,
            hashed_password=test_hashed_password,
        )
        assert user.id is None
        assert user.email == test_email
        assert user.hashed_password == test_hashed_password
        assert user.is_active is True

    def test_update_timestamp(self, test_email: str, test_hashed_password: str) -> None:
        """Test updating timestamp."""
        user = User(
            email=test_email,
            hashed_password=test_hashed_password,
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        old_timestamp = user.updated_at
        user.update_timestamp()
        assert user.updated_at > old_timestamp

    def test_deactivate(self, test_email: str, test_hashed_password: str) -> None:
        """Test deactivating user."""
        user = User(
            email=test_email,
            hashed_password=test_hashed_password,
            is_active=True,
        )
        user.deactivate()
        assert user.is_active is False

    def test_activate(self, test_email: str, test_hashed_password: str) -> None:
        """Test activating user."""
        user = User(
            email=test_email,
            hashed_password=test_hashed_password,
            is_active=False,
        )
        user.activate()
        assert user.is_active is True


class TestUserCreate:
    """Test UserCreate schema."""

    def test_user_create_valid(self, test_email: str, test_password: str) -> None:
        """Test creating UserCreate with valid data."""
        user_create = UserCreate(
            email=test_email,
            password=test_password,
        )
        assert user_create.email == test_email
        assert user_create.password == test_password

    def test_user_create_invalid_email(self, test_password: str) -> None:
        """Test creating UserCreate with invalid email."""
        with pytest.raises(ValueError, match="value is not a valid email"):
            UserCreate(
                email="invalid-email",
                password=test_password,
            )

    def test_user_create_short_password(
        self, test_email: str, short_password: str
    ) -> None:
        """Test creating UserCreate with short password."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            UserCreate(
                email=test_email,
                password=short_password,
            )


class TestUserUpdate:
    """Test UserUpdate schema."""

    def test_user_update_partial(self) -> None:
        """Test creating UserUpdate with partial data."""
        user_update = UserUpdate(email="new@example.com")
        assert user_update.email == "new@example.com"
        assert user_update.is_active is None

    def test_user_update_full(self) -> None:
        """Test creating UserUpdate with all fields."""
        user_update = UserUpdate(
            email="new@example.com",
            is_active=False,
        )
        assert user_update.email == "new@example.com"
        assert user_update.is_active is False

    def test_user_update_empty(self) -> None:
        """Test creating UserUpdate with no fields."""
        user_update = UserUpdate()
        assert user_update.email is None
        assert user_update.is_active is None
