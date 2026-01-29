from typing import Optional

from ..db.models.tenant import User


class TenantUserRepository:
    async def get_user_by_username(self, username: str, tenant_id: str) -> Optional[User]:
        return await User.get_or_none(username=username, tenant_id=tenant_id)

    async def create_user(self, username: str, password: str, tenant_id: str) -> User:
        user =  await User.create(username=username, password=password, tenant_id=tenant_id)
        print(user)
        return user
