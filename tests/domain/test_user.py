"""
Tests for domain entities.
"""

from datetime import UTC, datetime

import pytest

from app.domain.user import User, UserCreate, UserUpdate


TEST_HASHED_PASSWORD = "hashed_password_123"  # noqa: S105
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "secure_password_123"  # noqa: S105
SHORT_PASSWORD = "short"  # noqa: S105


class TestUser:
    """Test User domain entity."""

    def test_user_creation(self) -> None:
        """Test creating a user with all fields."""
        user = User(
            id=1,
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=UTC),
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        assert user.id == 1
        assert user.email == TEST_EMAIL
        assert user.hashed_password == TEST_HASHED_PASSWORD
        assert user.is_active is True

    def test_user_creation_defaults(self) -> None:
        """Test creating a user with default values."""
        user = User(
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
        )
        assert user.id is None
        assert user.email == TEST_EMAIL
        assert user.hashed_password == TEST_HASHED_PASSWORD
        assert user.is_active is True

    def test_update_timestamp(self) -> None:
        """Test updating timestamp."""
        user = User(
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        old_timestamp = user.updated_at
        user.update_timestamp()
        assert user.updated_at > old_timestamp

    def test_deactivate(self) -> None:
        """Test deactivating user."""
        user = User(
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
            is_active=True,
        )
        user.deactivate()
        assert user.is_active is False

    def test_activate(self) -> None:
        """Test activating user."""
        user = User(
            email=TEST_EMAIL,
            hashed_password=TEST_HASHED_PASSWORD,
            is_active=False,
        )
        user.activate()
        assert user.is_active is True


class TestUserCreate:
    """Test UserCreate schema."""

    def test_user_create_valid(self) -> None:
        """Test creating UserCreate with valid data."""
        user_create = UserCreate(
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
        )
        assert user_create.email == TEST_EMAIL
        assert user_create.password == TEST_PASSWORD

    def test_user_create_invalid_email(self) -> None:
        """Test creating UserCreate with invalid email."""
        with pytest.raises(ValueError, match="value is not a valid email"):
            UserCreate(
                email="invalid-email",
                password=TEST_PASSWORD,
            )

    def test_user_create_short_password(self) -> None:
        """Test creating UserCreate with short password."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            UserCreate(
                email=TEST_EMAIL,
                password=SHORT_PASSWORD,
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


class TestUser:
    """Test User domain entity."""

    def test_user_creation(self) -> None:
        """Test creating a user with all fields."""
        user = User(
            id=1,
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=UTC),
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert user.created_at == datetime(2023, 1, 1, tzinfo=UTC)
        assert user.updated_at == datetime(2023, 1, 1, tzinfo=UTC)

    def test_user_creation_defaults(self) -> None:
        """Test creating a user with default values."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
        )
        assert user.id is None
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_update_timestamp(self) -> None:
        """Test updating timestamp."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            updated_at=datetime(2023, 1, 1, tzinfo=UTC),
        )
        old_timestamp = user.updated_at
        user.update_timestamp()
        assert user.updated_at > old_timestamp

    def test_deactivate(self) -> None:
        """Test deactivating user."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True,
        )
        user.deactivate()
        assert user.is_active is False
        assert user.updated_at > user.created_at

    def test_activate(self) -> None:
        """Test activating user."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=False,
        )
        user.activate()
        assert user.is_active is True
        assert user.updated_at > user.created_at


class TestUserCreate:
    """Test UserCreate schema."""

    def test_user_create_valid(self) -> None:
        """Test creating UserCreate with valid data."""
        user_create = UserCreate(
            email="test@example.com",
            password="secure_password_123",
        )
        assert user_create.email == "test@example.com"
        assert user_create.password == "secure_password_123"

    def test_user_create_invalid_email(self) -> None:
        """Test creating UserCreate with invalid email."""
        with pytest.raises(ValueError):
            UserCreate(
                email="invalid-email",
                password="secure_password_123",
            )

    def test_user_create_short_password(self) -> None:
        """Test creating UserCreate with short password."""
        with pytest.raises(ValueError):
            UserCreate(
                email="test@example.com",
                password="short",
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
