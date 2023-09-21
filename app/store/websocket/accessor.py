import asyncio
import json
import uuid
import dataclasses
import typing as tp

from aiohttp import WSMsgType, web

from app.base.accessor import BaseAccessor
from app.store.websocket.models import Event, WebSocketSession


if tp.TYPE_CHECKING:
    from app.base.app import Request


class WSContext:
    def __init__(self, accessor: "WebSocketAccessor", request: "Request") -> None:
        self._accessor = accessor
        self._request = request
        self.connection_id: str | None = None

    async def __aenter__(self):
        self.connection_id = await self._accessor.open(self._request)
        return self.connection_id

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._accessor.close(connection_id=self.connection_id)
        

class WebSocketAccessor(BaseAccessor):
    class Meta:
        name = "websocket_accessor"

    CONNECTION_TIMEOUT_SECONDS = 20

    def _post_init_(self) -> None:
        self._connections: dict[str, WebSocketSession]= {}

    def _create_timeout(self, connection_id: str) -> asyncio.Task:
        def _done_callback(task: asyncio.Task) -> None:
            try:
                exc = task.exception()
            except asyncio.CancelledError:
                return

            if exc:
                self.logger.exception("Timeout task failed", exc_info=exc)

        task = asyncio.create_task(self._close_by_timeout(connection_id))
        task.add_done_callback(_done_callback)

        return task
    
    def _refresh_timeout(self, connection_id: str) -> None:
        self._connections[connection_id].timeout_task.cancel()
        self._connections[connection_id].timeout_task = self._create_timeout(connection_id)

    async def _close_by_timeout(self, connection_id: str) -> None:
        await asyncio.sleep(self.CONNECTION_TIMEOUT_SECONDS)
        await self.close(connection_id)

    async def open(self, request: "Request") -> str:
        client = web.WebSocketResponse()
        await client.prepare(request=request)

        connection_id = str(uuid.uuid4())
        self._connections[connection_id] = WebSocketSession(
            client=client,
            timeout_task=self._create_timeout(connection_id),
        )
        self.logger.info(f"Handling new connection {connection_id = }.")

        return connection_id
    
    async def close(self, connection_id: str) -> None:
        connection = self._connections.pop(connection_id, None)
        
        if connection is None:
            return
        
        self.logger.info(f"Closing {connection_id = }")

        if not connection.client.closed:
            await connection.client.close()

    async def notify_all(self, event: Event, except_of: list[str] = []) -> None:
        tasks = [
            self.push(connection_id=connection_id, event=event) 
            for connection_id in self._connections.keys() 
            if connection_id not in except_of
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [self.logger.warning(res) for res in results if isinstance(res, Exception)]

    async def push(self, connection_id: str, event: Event) -> None:
        data = json.dumps(dataclasses.asdict(event))
        self.logger.info(f"Sending {event} to {connection_id = }")
        await self._push(connection_id=connection_id, data=data)

    async def _push(self, connection_id: str, data: str) -> None:
        await self._connections[connection_id].client.send_str(data)

    async def read(self, connection_id: str) -> tp.AsyncIterator[Event]:
        async for message in self._connections[connection_id].client:
            self._refresh_timeout(connection_id)

            if message.type == WSMsgType.TEXT:

                message_data = message.json()

                yield Event(
                    kind=message_data["kind"],
                    payload=message_data["payload"]
                )