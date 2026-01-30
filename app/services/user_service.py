from fastapi import Depends

from app.core.exceptions import AppException
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.tenant_user_repository import TenantUserRepository


class UserService:
    def __init__(
        self,
        user_repository: TenantUserRepository = Depends(),
        organization_repository: OrganizationRepository = Depends()
    ):
        self.user_repository = user_repository
        self.organization_repository = organization_repository

    async def get_profile(self, username: str, tenant_id: str) -> dict:
        user = await self.user_repository.get_by_username(username, tenant_id)

        if not user:
            raise AppException("User not found.")

        organization = await self.organization_repository.get_by_tenant_code(tenant_id)

        return {
            "id": user.id,
            "username": user.username,
            "organization_name": organization.name if organization else None
        }

    async def update_profile(self, tenant_id: str, old_username: str, new_username: str) -> dict:
        user = await self.user_repository.get_by_username(new_username, tenant_id)

        if user:
            raise AppException("User with this username already exists.")

        updated_user = await self.user_repository.update_user(old_username, new_username, tenant_id)

        return {'username': updated_user.username}
