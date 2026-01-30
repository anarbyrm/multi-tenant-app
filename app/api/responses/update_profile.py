from pydantic import BaseModel


class UpdateProfileResponse(BaseModel):
    username: str
