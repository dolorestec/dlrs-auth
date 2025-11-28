from typing import Any
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.domain.user import User, UserCreate, UserUpdate


class TestUser:
    def test_user_creation(self, fake_email: str, fake_password: str) -> None:
        user = User(id=1, email=fake_email, hashed_password=fake_password)
        assert user.id == 1
        assert user.email == fake_email
        assert user.hashed_password == fake_password

    def test_user_equality(self, fake_email: str, fake_password: str) -> None:
        user1 = User(id=1, email=fake_email, hashed_password=fake_password)
        user2 = User(id=1, email=fake_email, hashed_password=fake_password)
        # Compare only relevant fields since timestamps differ
        assert user1.id == user2.id
        assert user1.email == user2.email
        assert user1.hashed_password == user2.hashed_password
        assert user1.is_active == user2.is_active

    def test_user_inequality(
        self, fake_email: str, fake_password: str, faker: Any
    ) -> None:
        user1 = User(id=1, email=fake_email, hashed_password=fake_password)
        user2 = User(id=2, email=faker.email(), hashed_password=faker.password())
        assert user1 != user2


class TestUserCreate:
    @pytest.mark.parametrize(
        ("email", "password"),
        [
            ("user@example.com", "password123"),
            ("test@domain.org", "securepass"),
            ("admin@test.net", "admin123"),
        ],
    )
    @patch("app.domain.user.pwd_context")
    def test_user_create_valid(
        self, mock_pwd_context: Any, email: str, password: str
    ) -> None:
        mock_pwd_context.hash.return_value = "hashed_password"
        user_create = UserCreate(email=email, password=password)
        assert user_create.email == email
        assert user_create.password == password

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "invalid-email",
            "@example.com",
            "user@",
            "",
        ],
    )
    def test_user_create_invalid_email(
        self, invalid_email: str, fake_password: str
    ) -> None:
        with pytest.raises(ValidationError):
            UserCreate(email=invalid_email, password=fake_password)

    def test_user_create_short_password(self, fake_email: str) -> None:
        with pytest.raises(ValidationError):
            UserCreate(email=fake_email, password="short")


class TestUserUpdate:
    def test_user_update_valid(self, fake_email: str) -> None:
        user_update = UserUpdate(email=fake_email)
        assert user_update.email == fake_email

    def test_user_update_invalid_email(self, fake_invalid_email: str) -> None:
        with pytest.raises(ValidationError):
            UserUpdate(email=fake_invalid_email)

    def test_user_update_optional_fields(self) -> None:
        user_update = UserUpdate()
        assert user_update.email is None


class TestHashPassword:
    @pytest.mark.parametrize(
        ("password", "expected_hash"),
        [
            ("password123", "hashed_password123"),
            ("securepass", "hashed_securepass"),
            ("admin123", "hashed_admin123"),
        ],
    )
    @patch("app.domain.user.pwd_context")
    def test_hash_password(
        self, mock_pwd_context: Any, password: str, expected_hash: str
    ) -> None:
        mock_pwd_context.hash.return_value = expected_hash
        result = User.hash_password(password)
        assert result == expected_hash
        mock_pwd_context.hash.assert_called_once_with(password)
