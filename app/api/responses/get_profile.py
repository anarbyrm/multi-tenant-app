from pydantic import BaseModel


class GetProfileResponse(BaseModel):
    id: int
    username: str
    organization_name: str
