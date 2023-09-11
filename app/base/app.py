import typing as tp

from aiohttp import web


if tp.TYPE_CHECKING:
    from logging import Logger
    from app.store import Store


class Application(web.Application):
    store: tp.Optional["Store"] = None
    logger: tp.Optional["Logger"] = None


class Request(web.Request):
    @property
    def app(self) -> "Application":
        return super().app


class View(web.View):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def app(self) -> "Application":
        return self.request.app

    @property
    def store(self) -> "Store":
        return self.app.store