from fastapi import APIRouter, Header
from fastapi.params import Depends

from app.api.requests.update_profile import UpdateProfileRequest
from app.api.responses.get_profile import GetProfileResponse
from app.api.responses.update_profile import UpdateProfileResponse
from app.services.user_service import UserService
from app.utils.authorize import get_current_tenant_user

router = APIRouter(prefix='/users')


@router.get('/me', response_model=GetProfileResponse)
async def get_profile(
    tenant_id: str = Header(..., alias="X-TENANT"),
    tenant_user: dict = Depends(get_current_tenant_user),
    user_service: UserService = Depends()
):
    return await user_service.get_profile(tenant_user['username'], tenant_id)


@router.patch('/me', response_model=UpdateProfileResponse)
async def update_profile(
    request: UpdateProfileRequest,
    tenant_id: str = Header(..., alias="X-TENANT"),
    tenant_user: dict = Depends(get_current_tenant_user),
    user_service: UserService = Depends()
):
    return await user_service.update_profile(tenant_id, tenant_user["username"], request.username)
