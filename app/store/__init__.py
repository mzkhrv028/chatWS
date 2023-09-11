import typing as tp

from app.store.ws.accessor import WebSocketAccessor


if tp.TYPE_CHECKING:
    from app.base.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.ws_accessor = WebSocketAccessor(app)


def setup_store(app: "Application") -> None:
    app.store = Store(app)