from typing import Optional

from app.db.models.main import Organization


class OrganizationRepository:
    async def get_by_name(self, name: str) -> Optional[Organization]:
        return await Organization.get_or_none(name=name)

    async def get_by_tenant_code(self, tenant_code: str) -> Optional[Organization]:
        return await Organization.get_or_none(tenant_code=tenant_code)

    async def create(self, name: str, user_id: int)-> Optional[Organization]:
        return await Organization.create(name=name, user_id=user_id)
