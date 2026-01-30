from fastapi import Depends

from app.core.exceptions import AppException
from app.db.models.main import Organization
from app.repositories.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository = Depends()):
        self.organization_repository = organization_repository

    async def create_organization(self, name: str, user_id: int) -> Organization:
        organization = await self.organization_repository.get_by_name(name)

        if organization:
            raise AppException("Organization already exists.")

        return await self.organization_repository.create(name, user_id)
