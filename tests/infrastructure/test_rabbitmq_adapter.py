"""
Tests for RabbitMQ event publisher adapter.
"""

from unittest.mock import AsyncMock, patch

import pytest
from aio_pika import DeliveryMode

from app.infrastructure.rabbitmq_adapter import RabbitMQEventPublisher


class TestRabbitMQEventPublisher:
    """Test RabbitMQ event publisher."""

    @pytest.fixture
    def publisher(self) -> RabbitMQEventPublisher:
        """RabbitMQ publisher instance."""
        return RabbitMQEventPublisher()

    @pytest.fixture
    def mock_connection(self) -> AsyncMock:
        """Mock RabbitMQ connection."""
        return AsyncMock()

    @pytest.fixture
    def mock_channel(self) -> AsyncMock:
        """Mock RabbitMQ channel."""
        return AsyncMock()

    @pytest.fixture
    def mock_exchange(self) -> AsyncMock:
        """Mock RabbitMQ exchange."""
        return AsyncMock()

    async def test_connect_success(
        self,
        publisher: RabbitMQEventPublisher,
        mock_connection: AsyncMock,
        mock_channel: AsyncMock,
        mock_exchange: AsyncMock,
        mock_settings,
    ) -> None:
        """Test successful connection to RabbitMQ."""
        with (
            patch(
                "aio_pika.connect_robust", return_value=mock_connection
            ) as mock_connect,
            patch("app.infrastructure.rabbitmq_adapter.settings", mock_settings),
        ):
            mock_connection.channel.return_value = mock_channel
            mock_channel.declare_exchange.return_value = mock_exchange

            await publisher.connect()

            mock_connect.assert_called_once_with(mock_settings.rabbitmq_url)
            mock_connection.channel.assert_called_once()
            mock_channel.declare_exchange.assert_called_once_with(
                name="auth_events",
                type="topic",
                durable=True,
            )
            assert publisher._connection == mock_connection  # noqa: SLF001
            assert publisher._channel == mock_channel  # noqa: SLF001
            assert publisher._exchange == mock_exchange  # noqa: SLF001

    async def test_connect_already_connected(
        self, publisher: RabbitMQEventPublisher, mock_connection: AsyncMock
    ) -> None:
        """Test connect when already connected."""
        publisher._connection = mock_connection  # noqa: SLF001

        await publisher.connect()

        # Should not attempt to connect again
        assert publisher._connection == mock_connection  # noqa: SLF001

    async def test_connect_failure(self, publisher: RabbitMQEventPublisher) -> None:
        """Test connection failure."""
        with (
            patch(
                "aio_pika.connect_robust", side_effect=Exception("Connection failed")
            ),
            pytest.raises(Exception, match="Connection failed"),
        ):
            await publisher.connect()

    async def test_disconnect(
        self,
        publisher: RabbitMQEventPublisher,
        mock_connection: AsyncMock,
        mock_channel: AsyncMock,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test disconnect from RabbitMQ."""
        publisher._connection = mock_connection  # noqa: SLF001
        publisher._channel = mock_channel  # noqa: SLF001
        publisher._exchange = mock_exchange  # noqa: SLF001

        await publisher.disconnect()

        mock_connection.close.assert_called_once()
        assert publisher._connection is None  # noqa: SLF001
        assert publisher._channel is None  # noqa: SLF001
        assert publisher._exchange is None  # noqa: SLF001

    async def test_disconnect_not_connected(
        self, publisher: RabbitMQEventPublisher
    ) -> None:
        """Test disconnect when not connected."""
        await publisher.disconnect()

        # Should not raise error
        assert publisher._connection is None  # noqa: SLF001

    async def test_publish_user_logged_in(
        self,
        publisher: RabbitMQEventPublisher,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test publishing user logged in event."""
        publisher._exchange = mock_exchange  # noqa: SLF001

        with patch.object(publisher, "_publish_event") as mock_publish:
            await publisher.publish_user_logged_in(1, "user@example.com", "192.168.1.1")

            mock_publish.assert_called_once_with(
                "auth.user.logged_in",
                {
                    "event_type": "user_logged_in",
                    "user_id": 1,
                    "email": "user@example.com",
                    "ip_address": "192.168.1.1",
                    "timestamp": None,
                },
            )

    async def test_publish_user_logged_in_no_ip(
        self,
        publisher: RabbitMQEventPublisher,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test publishing user logged in event without IP."""
        publisher._exchange = mock_exchange  # noqa: SLF001

        with patch.object(publisher, "_publish_event") as mock_publish:
            await publisher.publish_user_logged_in(1, "user@example.com")

            mock_publish.assert_called_once_with(
                "auth.user.logged_in",
                {
                    "event_type": "user_logged_in",
                    "user_id": 1,
                    "email": "user@example.com",
                    "ip_address": None,
                    "timestamp": None,
                },
            )

    async def test_publish_token_revoked(
        self,
        publisher: RabbitMQEventPublisher,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test publishing token revoked event."""
        publisher._exchange = mock_exchange  # noqa: SLF001

        with patch.object(publisher, "_publish_event") as mock_publish:
            await publisher.publish_token_revoked(1, "access")

            mock_publish.assert_called_once_with(
                "auth.token.revoked",
                {
                    "event_type": "token_revoked",
                    "user_id": 1,
                    "token_type": "access",
                    "timestamp": None,
                },
            )

    async def test_publish_password_changed(
        self,
        publisher: RabbitMQEventPublisher,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test publishing password changed event."""
        publisher._exchange = mock_exchange  # noqa: SLF001

        with patch.object(publisher, "_publish_event") as mock_publish:
            await publisher.publish_password_changed(1)

            mock_publish.assert_called_once_with(
                "auth.password.changed",
                {
                    "event_type": "password_changed",
                    "user_id": 1,
                    "timestamp": None,
                },
            )

    async def test_publish_event_with_connection(
        self,
        publisher: RabbitMQEventPublisher,
        mock_exchange: AsyncMock,
    ) -> None:
        """Test _publish_event with existing connection."""
        publisher._exchange = mock_exchange  # noqa: SLF001

        event_data = {"test": "data"}
        routing_key = "test.key"

        await publisher._publish_event(routing_key, event_data)  # noqa: SLF001

        mock_exchange.publish.assert_called_once()
        message = mock_exchange.publish.call_args[0][0]
        assert message.body == b'{"test": "data"}'
        assert message.delivery_mode == DeliveryMode.PERSISTENT
        assert message.content_type == "application/json"
        assert mock_exchange.publish.call_args[1]["routing_key"] == routing_key

    async def test_publish_event_without_connection(
        self,
        publisher: RabbitMQEventPublisher,
        mock_connection: AsyncMock,
        mock_channel: AsyncMock,
        mock_exchange: AsyncMock,
        mock_settings,
    ) -> None:
        """Test _publish_event without connection (should connect first)."""
        with (
            patch("aio_pika.connect_robust", return_value=mock_connection),
            patch("app.infrastructure.rabbitmq_adapter.settings", mock_settings),
        ):
            mock_connection.channel.return_value = mock_channel
            mock_channel.declare_exchange.return_value = mock_exchange

            event_data = {"test": "data"}
            routing_key = "test.key"

            await publisher._publish_event(routing_key, event_data)  # noqa: SLF001

            # Should have connected first
            mock_exchange.publish.assert_called_once()
