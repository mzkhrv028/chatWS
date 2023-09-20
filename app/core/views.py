from aiohttp import web

from app import BASE_DIR
from app.base.app import View
from app.store.websocket.accessor import WSContext


class IndexView(View):
    async def get(self):
        with open(BASE_DIR / "client" / "index.html", "r") as f:
            file = f.read()
            return web.Response(body=file, headers={"Content-type": "text/html"})
        

class WebSocketView(View):
    async def get(self) -> web.WebSocketResponse:
        async with WSContext(accessor=self.store.websocket, request=self.request) as connection_id:
            await self.store.chat.handle(connection_id)