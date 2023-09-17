import json
import uuid
import dataclasses
import typing as tp

from aiohttp import WSMessage, web

from app.base.accessor import BaseAccessor

if tp.TYPE_CHECKING:
    from app.base.app import Request


@dataclasses.dataclass
class Event:
    kind: str
    payload: dict

    def __str__(self) -> str:
        return f"Event <{self.kind}> with payload = {self.payload}"


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
        connection = self._connections.get(connection_id)
        self.logger.info(f"Closing {connection_id = }")
        if connection and not connection.closed:
            await connection.close()

    async def push(self, connection_id: str, event: Event) -> None:
        data = json.dumps(dataclasses.asdict(event))
        self.logger.info(f"Sending {event} to {connection_id = }")
        await self._push(connection_id=connection_id, data=data)

    async def _push(self, connection_id: str, data: str) -> None:
        await self._connections[connection_id].send_str(data)

    async def read(self, connection_id: str) -> WSMessage:
        async for message in self._connections[connection_id]:
            yield message