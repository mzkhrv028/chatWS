import logging

from aiohttp import web

from app.base.app import Application
from app.core.routes import setup_routes
from app.store import setup_store


logging.basicConfig(level=logging.INFO)

app = Application()


def setup_app() -> Application:
    app.logger = logging.getLogger()

    setup_store(app)
    setup_routes(app)

    return app


if __name__ == "__main__":
    web.run_app(setup_app(), host="localhost", port=8080)