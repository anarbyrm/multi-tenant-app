from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=125)
    password: str = Field(..., min_length=8, max_length=30)
