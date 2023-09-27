import typing as tp

from app import BASE_DIR
from app.core.views import ChatView, WebSocketView

if tp.TYPE_CHECKING:
    from app.base.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/connect", WebSocketView)
    app.router.add_static("/static", BASE_DIR / "client" / "static")
    app.router.add_view("/", ChatView)
