import logging
import typing as tp


if tp.TYPE_CHECKING:
    from app.base.app import Application


class BaseAccessor:
    class Meta:
        name = "base_accessor"

    def __init__(self, app: "Application"):
        self.app = app
        self.logger = app.logger.getChild(self.Meta.name)
        self._post_init_()

    def _post_init_(self) -> None:
        return None
    

class BaseManager(BaseAccessor):
    class Meta:
        name = "base_manager"