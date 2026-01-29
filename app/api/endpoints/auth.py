from typing import Optional

from fastapi import APIRouter, Response, Depends, Header, status

from app.api.requests.login import LoginRequest
from app.api.requests.register import RegisterRequest
from app.api.responses.login_response import LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth')


@router.post('/login', response_model=LoginResponse)
async def login(
    request: LoginRequest,
    tenant_id: Optional[str] = Header(default=None, alias="X-TENANT"),
    auth_service: AuthService = Depends()
):
    token = await auth_service.authenticate_user(request, tenant_id)
    return {"token": token}


@router.post('/register')
async def register(
    request: RegisterRequest,
    tenant_id: Optional[str] = Header(default=None, alias="X-TENANT"),
    auth_service: AuthService = Depends()
):
    await auth_service.register_user(request, tenant_id)
    return Response(status_code=status.HTTP_201_CREATED)
