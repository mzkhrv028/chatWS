import asyncio
from dataclasses import dataclass

from aiohttp import web


@dataclass
class Event:
    kind: str
    payload: dict

    def __str__(self) -> str:
        return f"Event <{self.kind}> with payload = {self.payload}"


@dataclass
class WebSocketSession:
    client: web.WebSocketResponse
    timeout_task: asyncio.Task
