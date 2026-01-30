import pytest

from app.core.exceptions import AppException
from app.repositories.organization_repository import OrganizationRepository
from app.services.organization_service import OrganizationService


@pytest.mark.asyncio
async def test_create_organization_success(mocker):
    organization_name = "test_org"
    tenant_code = "test_tenant_123"

    mock_repo = mocker.MagicMock(spec=OrganizationRepository)
    mock_repo.get_by_name = mocker.AsyncMock(return_value=None)

    mock_organization = mocker.MagicMock()
    mock_organization.id = 1
    mock_organization.name = organization_name
    mock_organization.tenant_code = tenant_code
    mock_organization.user_id = 1

    mock_repo.create = mocker.AsyncMock(return_value=mock_organization)

    service = OrganizationService(mock_repo)
    result = await service.create_organization(organization_name, 1)

    assert result.name == organization_name
    assert result.tenant_code == tenant_code


@pytest.mark.asyncio
async def test_create_organization_already_exists(mocker):
    organization_name = "test_org"

    mock_organization = mocker.MagicMock()
    mock_organization.id = 1
    mock_organization.name = organization_name
    mock_organization.tenant_code = "test_tenant_123"
    mock_organization.user_id = 1

    mock_repo = mocker.MagicMock(spec=OrganizationRepository)
    mock_repo.get_by_name.return_value = mock_organization

    service = OrganizationService(mock_repo)

    with pytest.raises(AppException) as exc:
        await service.create_organization(organization_name, 1)

    assert str(exc.value) == "Organization already exists."
