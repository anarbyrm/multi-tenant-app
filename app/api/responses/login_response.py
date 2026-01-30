from typing import List, Optional

from pydantic import BaseModel


class Organization(BaseModel):
    name: str
    tenant_code: str


class LoginResponse(BaseModel):
    token: str
    user_id: int
    username: str
    organizations: Optional[List[Organization]] = None
