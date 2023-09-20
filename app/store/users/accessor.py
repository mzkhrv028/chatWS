from app.base.accessor import BaseAccessor
from app.store.users.models import User


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
    
    async def remove(self, _id: str) -> User:
       return self._users.pop(_id)

    async def get(self, _id: str) -> User:
        return self._users[_id]
    
    async def update(self, _id: str, name: str) -> None:
        self._users[_id].name = name

    async def list(self) -> list[User]:
        return list(self._users.values())
    
