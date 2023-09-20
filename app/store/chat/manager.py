import dataclasses
from datetime import datetime

from app.base.accessor import BaseManager
from app.store.websocket.models import Event


class ChatServerEventKind:
    INITIAL = "initial"
    ADD = "add"
    SEND = "send"
    REMOVE = "remove"


class ChatClientEventKind:
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    SEND = "send"
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
                case ChatClientEventKind.SEND:
                    await self._handle_message(
                        connection_id=connection_id,
                        payload=event.payload,
                    )
                case ChatClientEventKind.DISCONNECT:
                    await self._handle_disconnect(
                        connection_id=connection_id
                    )
                case _:
                    raise NotImplementedError
                
    async def _handle_connect(self, connection_id: str, payload: dict[str, str]) -> None:
        user = await self.app.store.users.create(connection_id, payload.get("name"))
        self.logger.info(f"{user} connected")
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
        user = await self.app.store.users.remove(connection_id)
        self.logger.info(f"User with id {connection_id} removed")
        await self.app.store.websocket.notify_all(
            event=Event(
                kind=ChatServerEventKind.REMOVE,
                payload={
                    "id": user.id,
                    "name": user.name
                },
            ),
            except_of=[connection_id],
        )

    async def _handle_message(self, connection_id: str, payload: dict[str, str]) -> None:
        self.logger.info(f"Message {payload['message']} sent from {connection_id}")
        await self.app.store.websocket.notify_all(
            event=Event(
                kind=ChatServerEventKind.SEND,
                payload={
                    "id": connection_id,
                    "name": payload["name"],
                    "message": payload["message"],
                    "time": f"{datetime.now():%H:%M:%S}",
                },
            ),
        )

    async def _on_connect(self, connection_id: str) -> None:
        users = await self.app.store.users.list()
        await self.app.store.websocket.push(connection_id=connection_id, event=Event(
                kind=ChatServerEventKind.INITIAL,
                payload={
                    "id": connection_id,
                    "users": [dataclasses.asdict(user) for user in users],
                }
            )
        )
