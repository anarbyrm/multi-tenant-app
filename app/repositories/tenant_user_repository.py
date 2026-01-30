from typing import Optional

from ..core.exceptions import AppException
from ..db.models.tenant import User


class TenantUserRepository:
    async def get_by_id(self, user_id: str, tenant_id: str) -> Optional[User]:
        return await User.get_or_none(id=user_id, tenant_id=tenant_id)

    async def get_by_username(self, username: str, tenant_id: str) -> Optional[User]:
        return await User.get_or_none(username=username, tenant_id=tenant_id)

    async def create_user(self, username: str, password: str, tenant_id: str) -> User:
        return await User.create(username=username, password=password, tenant_id=tenant_id)

    async def update_user(self, old_username: str, new_username: str, tenant_id: str) -> User:
        user = await self.get_by_username(old_username, tenant_id)

        if not user:
            raise AppException("User not found.")

        user.username = new_username
        await user.save()
        return user
