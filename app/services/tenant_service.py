from fastapi.params import Depends

from app.repositories.tenant_repository import TenantRepository


class TenantService:
    def __init__(self, repository: TenantRepository = Depends()):
        self.repository = repository
