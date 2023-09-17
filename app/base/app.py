import typing as tp
from logging import Logger

from aiohttp import web

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