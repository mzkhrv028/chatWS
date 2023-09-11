from aiohttp import WSMsgType, web

from app import BASE_DIR
from app.base.app import View


class IndexView(View):
    async def get(self):
        with open(BASE_DIR / "client" / "index.html", "r") as f:
            file = f.read()
            return web.Response(body=file, headers={"Content-type": "text/html"})
        

class WebSocketView(View):
    async def get(self) -> web.WebSocketResponse:
        await self.store.ws_accessor.open(self.request)