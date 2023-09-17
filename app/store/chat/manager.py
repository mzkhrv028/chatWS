from app.base.accessor import BaseManager
from app.store.websocket.accessor import Event


class ChatServerEventKind:
    INITIAL = "initial"
    ADD = "add"
    SEND = "send"
    REMOVE = "remove"


class ChatClientEventKind:
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    PING = "ping"


class ChatManager(BaseManager):
    class Meta:
        name = "chat_manager"

    async def handle(self, connection_id: str) -> None:
        await self._on_connect(connection_id=connection_id)

        async for message in self.app.store.websocket.read(connection_id):
            self.logger.info(message)

    async def _on_connect(self, connection_id: str) -> None:
        self.logger.info("Sending initial message")
        user = await self.app.store.users.create(connection_id, "Name")
        await self.app.store.websocket.push(connection_id=connection_id, event=Event(
                kind="initial",
                payload={
                    "id": connection_id,
                    "users": [],
                }
            )
        )
