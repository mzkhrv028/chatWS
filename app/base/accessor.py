from logging import getLogger
import typing as tp


if tp.TYPE_CHECKING:
    from app.base.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", *args, **kwargs):
        self.app = app
        self.logger = getLogger("accessor")