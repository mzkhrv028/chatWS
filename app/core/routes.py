import typing as tp

from app.core.views import IndexView, WebSocketView


if tp.TYPE_CHECKING:
    from app.base.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/", IndexView)
    app.router.add_view("/connect", WebSocketView)