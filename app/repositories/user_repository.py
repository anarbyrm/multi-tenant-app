from typing import Optional

from ..db.models.main import User


class UserRepository:
    async def get_by_username(self, username: str) -> Optional[User]:
        return await (User.filter(username=username)
                      .prefetch_related("organizations")
                      .first())

    async def get_by_id(self, user_id: str) -> Optional[User]:
        return await (User.filter(id=user_id)
                      .prefetch_related("organizations")
                      .first())

    async def create_user(self, username: str, password: str) -> User:
        return await User.create(username=username, password=password)
