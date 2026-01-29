from fastapi import APIRouter, Depends, status

from app.api.requests.create_organization import CreateOrganizationRequest
from app.api.responses.create_organization import CreateOrganizationResponse
from app.services.organization_service import OrganizationService
from app.utils.authorize import get_current_user

router = APIRouter(prefix='/organizations')


@router.post('/', response_model=CreateOrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    request: CreateOrganizationRequest,
    current_user: dict = Depends(get_current_user),
    organization_service: OrganizationService = Depends()
):
    return await organization_service.create_organization(request.name, current_user)
