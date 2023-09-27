import typing as tp

from app.store.chat.manager import ChatManager
from app.store.users.accessor import UsersAccessor
from app.store.websocket.accessor import WebSocketAccessor

if tp.TYPE_CHECKING:
    from app.base.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.websocket = WebSocketAccessor(app)
        self.users = UsersAccessor(app)
        self.chat = ChatManager(app)


def setup_store(app: "Application") -> None:
    app.store = Store(app)
