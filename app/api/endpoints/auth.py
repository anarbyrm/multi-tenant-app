from typing import Optional

from fastapi import APIRouter, Response, Depends, Header, status

from app.api.requests.login import LoginRequest
from app.api.requests.register import RegisterRequest
from app.api.responses.login_response import LoginResponse
from app.services.auth_service import AuthService
from app.utils.authorize import authorize_current_tenant

router = APIRouter(prefix='/auth', dependencies=[Depends(authorize_current_tenant)])


@router.post('/login', response_model=LoginResponse, response_model_exclude_unset=True)
async def login(
    request: LoginRequest,
    tenant_id: Optional[str] = Header(default=None, alias="X-TENANT"),
    auth_service: AuthService = Depends()
):
    return await auth_service.authenticate_user(request, tenant_id)


@router.post('/register')
async def register(
    request: RegisterRequest,
    tenant_id: Optional[str] = Header(default=None, alias="X-TENANT"),
    auth_service: AuthService = Depends()
):
    await auth_service.register_user(request, tenant_id)
    return Response(status_code=status.HTTP_201_CREATED)
