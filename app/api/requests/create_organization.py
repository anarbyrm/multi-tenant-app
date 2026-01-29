from pydantic import BaseModel, Field


class CreateOrganizationRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=150)
