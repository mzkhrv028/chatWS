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

        async for event in self.app.store.websocket.read(connection_id):
            match event.kind:
                case ChatClientEventKind.CONNECT:
                    await self._handle_connect(
                        connection_id=connection_id,
                        payload=event.payload,
                    )
                case ChatClientEventKind.PING:
                    pass
                case ChatClientEventKind.DISCONNECT:
                    await self._handle_disconnect(
                        connection_id=connection_id
                    )
                case _:
                    raise NotImplementedError
                
    async def _handle_connect(self, connection_id: str, payload: str):
        user = await self.app.store.users.create(connection_id, "name")
        self.logger.info(f"New {user} created")
        await self.app.store.websocket.notify_all(
            event=Event(
                kind=ChatServerEventKind.ADD,
                payload={
                    "id": user.id,
                    "name": user.name,
                },
            ),
            except_of=[connection_id],
        )

    async def _handle_disconnect(self, connection_id: str):
        await self.app.store.users.remove(connection_id)
        self.logger.info(f"User with id {connection_id} removed")
        await self.app.store.websocket.notify_all(
            event=Event(
                kind=ChatServerEventKind.REMOVE,
                payload={
                    "id": connection_id,
                },
            ),
            except_of=[connection_id],
        )

    async def _on_connect(self, connection_id: str) -> None:
        await self.app.store.websocket.push(connection_id=connection_id, event=Event(
                kind=ChatServerEventKind.INITIAL,
                payload={
                    "id": connection_id,
                    "users": [],
                }
            )
        )
