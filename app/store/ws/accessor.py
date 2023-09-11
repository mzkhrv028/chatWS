from aiohttp import web

from app.base.accessor import BaseAccessor
from app.base.app import Application, Request


class WebSocketAccessor(BaseAccessor):
    class Meta:
        name = "websocket_accessor"

    def __init__(self, app: Application, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self._username_to_writer = {}

    async def open(self, request: "Request") -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request=request)
        self.logger.info("Process new connection.")
        return ws
