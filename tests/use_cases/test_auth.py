"""
Tests for authentication use cases.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.domain.user import User
from app.infrastructure.interfaces import ICache, IEventPublisher, IUserRepository
from app.use_cases.auth import (
    LoginRequest,
    LoginUseCase,
    RefreshTokenUseCase,
    TokenResponse,
    ValidateTokenUseCase,
)


class TestLoginUseCase:
    """Test LoginUseCase."""

    @pytest.fixture
    def mock_user_repository(self) -> IUserRepository:
        """Mock user repository."""
        return MagicMock(spec=IUserRepository)

    @pytest.fixture
    def mock_cache(self) -> ICache:
        """Mock cache."""
        return MagicMock(spec=ICache)

    @pytest.fixture
    def mock_event_publisher(self) -> IEventPublisher:
        """Mock event publisher."""
        return MagicMock(spec=IEventPublisher)

    @pytest.fixture
    def login_use_case(
        self,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        mock_event_publisher: IEventPublisher,
    ) -> LoginUseCase:
        """Login use case instance."""
        return LoginUseCase(mock_user_repository, mock_cache, mock_event_publisher)

    @pytest.fixture
    def active_user(
        self,
        fake_email: str,
        fake_password: str,
        fake_user_id: int,
    ) -> User:
        """Active user fixture."""
        return User(
            id=fake_user_id,
            email=fake_email,
            hashed_password=User.hash_password(fake_password),
            is_active=True,
        )

    async def test_successful_login(  # noqa: PLR0913
        self,
        login_use_case: LoginUseCase,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        mock_event_publisher: IEventPublisher,
        active_user: User,
        fake_email: str,
        fake_password: str,
        fake_user_id: int,
    ) -> None:
        """Test successful login."""
        # Setup mocks
        mock_user_repository.get_by_email = AsyncMock(return_value=active_user)  # type: ignore[method-assign]
        mock_cache.incr = AsyncMock(return_value=1)  # type: ignore[method-assign]
        mock_cache.expire = AsyncMock()  # type: ignore[method-assign]
        mock_cache.delete = AsyncMock()  # type: ignore[method-assign]
        mock_event_publisher.publish_user_logged_in = AsyncMock()  # type: ignore[method-assign]

        # Execute
        request = LoginRequest(email=fake_email, password=fake_password)
        response = await login_use_case.execute(request)

        # Assert
        assert isinstance(response, TokenResponse)
        assert response.access_token is not None
        assert response.refresh_token is not None
        assert response.token_type == "bearer"

        # Verify mocks called
        mock_user_repository.get_by_email.assert_called_once_with(fake_email)
        mock_cache.incr.assert_called_once_with(f"login_attempts:{fake_email}")
        mock_cache.expire.assert_called_once()
        mock_cache.delete.assert_called_once_with(f"login_attempts:{fake_email}")
        mock_event_publisher.publish_user_logged_in.assert_called_once_with(
            fake_user_id, fake_email
        )

    async def test_login_user_not_found(
        self,
        login_use_case: LoginUseCase,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        fake_email: str,
        fake_password: str,
    ) -> None:
        """Test login with non-existent user."""
        # Setup mocks
        mock_user_repository.get_by_email = AsyncMock(return_value=None)  # type: ignore[method-assign]
        mock_cache.incr = AsyncMock(return_value=1)  # type: ignore[method-assign]
        mock_cache.expire = AsyncMock()  # type: ignore[method-assign]

        # Execute and assert
        request = LoginRequest(email=fake_email, password=fake_password)
        with pytest.raises(ValueError, match="Invalid credentials"):
            await login_use_case.execute(request)

        # Verify mocks called
        mock_user_repository.get_by_email.assert_called_once_with(fake_email)
        mock_cache.incr.assert_called_once_with(f"login_attempts:{fake_email}")
        mock_cache.expire.assert_called_once()

    async def test_login_inactive_user(  # noqa: PLR0913
        self,
        login_use_case: LoginUseCase,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        fake_email: str,
        fake_password: str,
        mock_pwd_context_hash,
    ) -> None:
        """Test login with inactive user."""
        # Setup mocks
        inactive_user = User(
            id=1,
            email=fake_email,
            hashed_password=mock_pwd_context_hash.return_value,
            is_active=False,
        )
        mock_user_repository.get_by_email = AsyncMock(return_value=inactive_user)  # type: ignore[method-assign]
        mock_cache.incr = AsyncMock(return_value=1)  # type: ignore[method-assign]
        mock_cache.expire = AsyncMock()  # type: ignore[method-assign]

        # Execute and assert
        request = LoginRequest(email=fake_email, password=fake_password)
        with pytest.raises(ValueError, match="Invalid credentials"):
            await login_use_case.execute(request)

    async def test_login_wrong_password(  # noqa: PLR0913
        self,
        login_use_case: LoginUseCase,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        active_user: User,
        fake_email: str,
        mock_pwd_context_verify,
    ) -> None:
        """Test login with wrong password."""
        # Setup mocks
        mock_user_repository.get_by_email = AsyncMock(return_value=active_user)  # type: ignore[method-assign]
        mock_cache.incr = AsyncMock(return_value=1)  # type: ignore[method-assign]
        mock_cache.expire = AsyncMock()  # type: ignore[method-assign]
        mock_pwd_context_verify.return_value = False  # Wrong password

        # Execute and assert
        request = LoginRequest(email=fake_email, password="wrong_password")
        with pytest.raises(ValueError, match="Invalid credentials"):
            await login_use_case.execute(request)

        # Verify rate limit not reset
        mock_cache.delete.assert_not_called()  # type: ignore[attr-defined]

    async def test_login_rate_limit_exceeded(  # noqa: PLR0913
        self,
        login_use_case: LoginUseCase,
        mock_user_repository: IUserRepository,
        mock_cache: ICache,
        fake_email: str,
        fake_password: str,
        mock_settings,
    ) -> None:
        """Test login when rate limit is exceeded."""
        # Setup mocks
        mock_cache.incr = AsyncMock(  # type: ignore[method-assign]
            return_value=6
        )  # Exceeds limit
        mock_user_repository.get_by_email = (  # type: ignore[method-assign]
            AsyncMock()
        )  # Should not be called

        # Patch settings in the use case module
        with patch("app.use_cases.auth.settings", mock_settings):
            # Execute and assert
            request = LoginRequest(email=fake_email, password=fake_password)
            with pytest.raises(
                ValueError, match=r"Too many login attempts. Please try again later."
            ):
                await login_use_case.execute(request)

        # Verify user lookup not called
        mock_user_repository.get_by_email.assert_not_called()


class TestValidateTokenUseCase:
    """Test ValidateTokenUseCase."""

    @pytest.fixture
    def validate_use_case(self) -> ValidateTokenUseCase:
        """Validate token use case instance."""
        return ValidateTokenUseCase()

    async def test_execute_placeholder(
        self, validate_use_case: ValidateTokenUseCase
    ) -> None:
        """Test placeholder implementation."""
        result = await validate_use_case.execute("test_token")
        assert result == {"user_id": "1", "email": "user@example.com"}


class TestRefreshTokenUseCase:
    """Test RefreshTokenUseCase."""

    @pytest.fixture
    def refresh_use_case(self) -> RefreshTokenUseCase:
        """Refresh token use case instance."""
        return RefreshTokenUseCase()

    async def test_execute_placeholder(
        self, refresh_use_case: RefreshTokenUseCase
    ) -> None:
        """Test placeholder implementation."""
        result = await refresh_use_case.execute("refresh_token")
        assert isinstance(result, TokenResponse)
        assert result.access_token == "new_access_token"
        assert result.refresh_token == "new_refresh_token"
        assert result.token_type == "bearer"
