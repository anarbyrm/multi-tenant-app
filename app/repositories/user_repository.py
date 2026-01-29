from typing import Optional

from ..db.models.main import User


class UserRepository:
    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await User.get_or_none(username=username)

    async def create_user(self, username, password) -> User:
        return await User.create(username=username, password=password)
