"""
RabbitMQ adapter for publishing authentication events.

Following Clean Architecture principles.
"""

from __future__ import annotations

import json
from typing import Any

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from structlog import get_logger

from app.core.config import settings
from app.infrastructure.interfaces import IEventPublisher

logger = get_logger(__name__)


class RabbitMQEventPublisher(IEventPublisher):
    """RabbitMQ event publisher adapter."""

    def __init__(self) -> None:
        self._connection: aio_pika.Connection | None = None
        self._channel: aio_pika.Channel | None = None
        self._exchange: aio_pika.Exchange | None = None

    async def connect(self) -> None:
        """Connect to RabbitMQ and setup exchange."""
        if self._connection:
            return

        try:
            self._connection = await aio_pika.connect_robust(settings.rabbitmq_url)
            self._channel = await self._connection.channel()

            # Declare exchange for authentication events
            self._exchange = await self._channel.declare_exchange(
                name="auth_events",
                type=ExchangeType.TOPIC,
                durable=True,
            )

            logger.info("Connected to RabbitMQ and declared auth_events exchange")
        except Exception:
            logger.exception("Failed to connect to RabbitMQ")
            raise

    async def disconnect(self) -> None:
        """Disconnect from RabbitMQ."""
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
            self._exchange = None
            logger.info("Disconnected from RabbitMQ")

    async def _publish_event(
        self, routing_key: str, event_data: dict[str, Any]
    ) -> None:
        """Publish event to exchange."""
        if not self._exchange:
            await self.connect()
            if not self._exchange:
                logger.error("Failed to establish RabbitMQ connection")
                return

        message_body = json.dumps(event_data).encode()
        message = Message(
            body=message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
        )

        await self._exchange.publish(message, routing_key=routing_key)
        logger.info("Published event", routing_key=routing_key, event_data=event_data)

    async def publish_user_logged_in(
        self, user_id: int, email: str, ip_address: str | None = None
    ) -> None:
        """Publish user login event."""
        event_data = {
            "event_type": "user_logged_in",
            "user_id": user_id,
            "email": email,
            "ip_address": ip_address,
            "timestamp": None,  # Will be set by consumer or message timestamp
        }
        await self._publish_event("auth.user.logged_in", event_data)

    async def publish_token_revoked(self, user_id: int, token_type: str) -> None:
        """Publish token revocation event."""
        event_data = {
            "event_type": "token_revoked",
            "user_id": user_id,
            "token_type": token_type,
            "timestamp": None,
        }
        await self._publish_event("auth.token.revoked", event_data)

    async def publish_password_changed(self, user_id: int) -> None:
        """Publish password change event."""
        event_data = {
            "event_type": "password_changed",
            "user_id": user_id,
            "timestamp": None,
        }
        await self._publish_event("auth.password.changed", event_data)


# Global instance
rabbitmq_publisher = RabbitMQEventPublisher()
