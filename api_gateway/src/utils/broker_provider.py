from typing import Any
from faststream.rabbit import RabbitBroker


class BrokerProvider:
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def get_broker(self) -> RabbitBroker:
        if not self._broker.setup:
            await self._broker.connect()
        return self._broker

    async def rpc(
        self,
        queue: str,
        payload: Any,
        *,
        exchange: str | None = None,
        timeout: float | None = 5.0,
    ) -> Any:
        """
        Publish payload to queue using RabbitMQ Direct-Reply-To and return the decoded response.

        Raises asyncio.TimeoutError if the service doesn’t answer before timeout expires.
        """
        msg = await self._broker.request(
            message=payload,
            queue=queue,
            exchange=exchange,
            timeout=timeout,
        )
        return await msg.decode()
