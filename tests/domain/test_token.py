"""
Tests for Token domain entity.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from jose import jwt  # type: ignore[import]
import pytest

from app.domain.token import Token, TokenData


class TestToken:
    """Test Token domain entity."""

    def test_create_access_token_default_expiry(
        self, mock_settings, fake_subject: str
    ) -> None:
        """Test creating access token with default expiry."""
        with patch("app.domain.token.settings", mock_settings):
            token = Token.create_access_token(fake_subject)

            assert isinstance(token, str)
            assert len(token) > 0

            # Decode to verify content
            decoded = Token.decode_token(token)
            assert decoded["sub"] == fake_subject
            assert decoded["type"] == "access"
            assert "exp" in decoded

    def test_create_access_token_custom_expiry(
        self, mock_settings, fake_subject: str
    ) -> None:
        """Test creating access token with custom expiry."""
        with patch("app.domain.token.settings", mock_settings):
            custom_delta = timedelta(minutes=60)
            token = Token.create_access_token(fake_subject, custom_delta)

            assert isinstance(token, str)

            decoded = Token.decode_token(token)
            assert decoded["sub"] == fake_subject
            assert decoded["type"] == "access"

    def test_create_refresh_token_default_expiry(
        self, mock_settings, fake_subject: str
    ) -> None:
        """Test creating refresh token with default expiry."""
        with patch("app.domain.token.settings", mock_settings):
            token = Token.create_refresh_token(fake_subject)

            assert isinstance(token, str)

            decoded = Token.decode_token(token)
            assert decoded["sub"] == fake_subject
            assert decoded["type"] == "refresh"

    def test_create_refresh_token_custom_expiry(
        self, mock_settings, fake_subject: str
    ) -> None:
        """Test creating refresh token with custom expiry."""
        with patch("app.domain.token.settings", mock_settings):
            custom_delta = timedelta(days=30)
            token = Token.create_refresh_token(fake_subject, custom_delta)

            assert isinstance(token, str)

            decoded = Token.decode_token(token)
            assert decoded["sub"] == fake_subject
            assert decoded["type"] == "refresh"

    def test_create_token_pair(self, mock_settings, fake_subject: str) -> None:
        """Test creating token pair."""
        with patch("app.domain.token.settings", mock_settings):
            token_pair = Token.create_token_pair(fake_subject)

            assert isinstance(token_pair, Token)
            assert token_pair.access_token is not None
            assert token_pair.refresh_token is not None
            assert token_pair.token_type == "bearer"
            assert isinstance(token_pair.expires_at, datetime)

            # Verify access token
            access_decoded = Token.decode_token(token_pair.access_token)
            assert access_decoded["sub"] == fake_subject
            assert access_decoded["type"] == "access"

            # Verify refresh token
            refresh_decoded = Token.decode_token(token_pair.refresh_token)
            assert refresh_decoded["sub"] == fake_subject
            assert refresh_decoded["type"] == "refresh"

    def test_token_creation(self, faker) -> None:
        """Test creating Token instance."""
        fake_token = faker.pystr()
        expires_at = datetime.now(UTC) + timedelta(minutes=30)

        token = Token(
            access_token=fake_token,
            expires_at=expires_at,
            refresh_token=faker.pystr(),
        )

        assert token.access_token == fake_token
        assert token.expires_at == expires_at
        assert token.refresh_token is not None
        assert token.token_type == "bearer"

    def test_token_creation_defaults(self, faker) -> None:
        """Test creating Token with defaults."""
        fake_token = faker.pystr()
        expires_at = datetime.now(UTC) + timedelta(minutes=30)

        token = Token(
            access_token=fake_token,
            expires_at=expires_at,
        )

        assert token.access_token == fake_token
        assert token.expires_at == expires_at
        assert token.refresh_token is None
        assert token.token_type == "bearer"

    def test_is_expired_false(self, faker) -> None:
        """Test is_expired property when token is not expired."""
        future_time = datetime.now(UTC) + timedelta(minutes=30)

        token = Token(
            access_token=faker.pystr(),
            expires_at=future_time,
        )

        assert token.is_expired is False

    def test_is_expired_true(self, faker) -> None:
        """Test is_expired property when token is expired."""
        past_time = datetime.now(UTC) - timedelta(minutes=30)

        token = Token(
            access_token=faker.pystr(),
            expires_at=past_time,
        )

        assert token.is_expired is True

    def test_decode_token(self, mock_settings, fake_subject: str) -> None:
        """Test decoding a valid token."""
        with patch("app.domain.token.settings", mock_settings):
            token_str = Token.create_access_token(fake_subject)
            decoded = Token.decode_token(token_str)

            assert decoded["sub"] == fake_subject
            assert decoded["type"] == "access"
            assert "exp" in decoded

    def test_decode_invalid_token(self, mock_settings) -> None:
        """Test decoding an invalid token."""
        with (
            patch("app.domain.token.settings", mock_settings),
            pytest.raises(jwt.DecodeError),
        ):
            Token.decode_token("invalid_token")


class TestTokenData:
    """Test TokenData model."""

    def test_token_data_creation(self, fake_subject: str) -> None:
        """Test creating TokenData instance."""
        exp_time = datetime.now(UTC) + timedelta(minutes=30)

        token_data = TokenData(
            sub=fake_subject,
            exp=exp_time,
            type="access",
        )

        assert token_data.sub == fake_subject
        assert token_data.exp == exp_time
        assert token_data.type == "access"
