import dataclasses
from app.base.accessor import BaseAccessor


@dataclasses.dataclass
class User:
    id: str
    name: str


class UsersAccessor(BaseAccessor):
    class Meta:
        name = "users_accessor"

    def _post_init_(self) -> None:
        self._users: dict[str, User] = {}

    async def create(self, _id: str, name: str) -> User:
        self._users[_id] = User(
            id=_id,
            name=name,
        )
        return self._users[_id]
    
    async def remove(self, _id: str) -> None:
        del self._users[_id]

    async def get(self, _id: str) -> User:
        return self._users[_id]
    
    async def update(self, _id: str, name: str) -> None:
        self._users[_id].name = name
    
