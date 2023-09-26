from aiohttp import web

from app import BASE_DIR
from app.base.app import View
from app.store.websocket.accessor import WSContext


class ChatView(View):
    async def get(self) -> web.FileResponse:
        return web.FileResponse(
            path=BASE_DIR / "client" / "static" / "templates" / "chat.html",
            headers={"Content-Type": "text/html"},
        )
    

class WebSocketView(View):
    async def get(self) -> web.WebSocketResponse:
        async with WSContext(accessor=self.store.websocket, request=self.request) as connection_id:
            await self.store.chat.handle(connection_id)