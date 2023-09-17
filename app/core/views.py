from aiohttp import web

from app import BASE_DIR
from app.base.app import View
from app.store.websocket.accessor import Event


class IndexView(View):
    async def get(self):
        with open(BASE_DIR / "client" / "index.html", "r") as f:
            file = f.read()
            return web.Response(body=file, headers={"Content-type": "text/html"})
        

class WebSocketView(View):
    async def get(self) -> web.WebSocketResponse:
        connection_id = await self.store.websocket.open(self.request)
        await self.store.chat.handle(connection_id)
        await self.store.websocket.close(connection_id)