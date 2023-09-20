import asyncio
import json
import uuid
import dataclasses
import typing as tp

from aiohttp import web

from app.base.accessor import BaseAccessor
from app.store.websocket.models import Event


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

    def _post_init_(self) -> None:
        self._connections: dict[str, web.WebSocketResponse]= {}

    async def open(self, request: "Request") -> str:
        ws = web.WebSocketResponse()
        await ws.prepare(request=request)

        connection_id = str(uuid.uuid4())
        self._connections[connection_id] = ws
        self.logger.info(f"Handling new connection {connection_id = }.")

        return connection_id
    
    async def close(self, connection_id: str) -> None:
        connection = self._connections.pop(connection_id, None)
        
        if connection is None:
            return
        
        self.logger.info(f"Closing {connection_id = }")

        if not connection.closed:
            await connection.close()

    async def notify_all(self, event: Event, except_of: list[str] | None = None) -> None:
        futures = []
        for connection_id in self._connections:
            if except_of and connection_id in except_of:
                continue
            futures.append(self.push(connection_id=connection_id, event=event))
        
        await asyncio.gather(*futures)
            

    async def push(self, connection_id: str, event: Event) -> None:
        data = json.dumps(dataclasses.asdict(event))
        self.logger.info(f"Sending {event} to {connection_id = }")
        await self._push(connection_id=connection_id, data=data)

    async def _push(self, connection_id: str, data: str) -> None:
        await self._connections[connection_id].send_str(data)

    async def read(self, connection_id: str) -> tp.AsyncIterator[Event]:
        async for message in self._connections[connection_id]:
            message_data = message.json()

            yield Event(
                kind=message_data["kind"],
                payload=message_data["payload"]
            )