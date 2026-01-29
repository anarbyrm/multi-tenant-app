from pydantic import BaseModel, UUID4


class CreateOrganizationResponse(BaseModel):
    id: int
    name: str
    tenant_code: UUID4

