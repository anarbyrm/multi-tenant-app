import pytest
from app.core.exceptions import AppException
from app.services.user_service import UserService
from app.repositories.tenant_user_repository import TenantUserRepository
from app.repositories.organization_repository import OrganizationRepository


@pytest.mark.asyncio
async def test_get_profile_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=TenantUserRepository)
    mock_org_repo = mocker.MagicMock(spec=OrganizationRepository)

    username = "test_user"
    user_id = 1
    organization_name = "test_organization"

    user = mocker.MagicMock()
    user.id = user_id
    user.username = username
    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=user)

    org = mocker.MagicMock()
    org.name = organization_name
    mock_org_repo.get_by_tenant_code = mocker.AsyncMock(return_value=org)

    service = UserService(user_repository=mock_user_repo, organization_repository=mock_org_repo)

    result = await service.get_profile(username, tenant_id="tenant1")

    assert result == {"id": user_id, "username": username, "organization_name": organization_name}


@pytest.mark.asyncio
async def test_get_profile_user_not_found(mocker):
    mock_user_repo = mocker.MagicMock(spec=TenantUserRepository)
    mock_org_repo = mocker.MagicMock(spec=OrganizationRepository)

    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=None)

    service = UserService(user_repository=mock_user_repo, organization_repository=mock_org_repo)

    with pytest.raises(AppException) as exc:
        await service.get_profile("test_user", tenant_id="t")

    assert str(exc.value) == "User not found."


@pytest.mark.asyncio
async def test_update_profile_conflict_username_exists(mocker):
    mock_user_repo = mocker.MagicMock(spec=TenantUserRepository)
    mock_org_repo = mocker.MagicMock(spec=OrganizationRepository)

    existing = mocker.MagicMock()
    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=existing)

    service = UserService(user_repository=mock_user_repo, organization_repository=mock_org_repo)

    with pytest.raises(AppException) as exc:
        await service.update_profile("test_tenant", old_username="old", new_username="new")

    assert str(exc.value) == "User with this username already exists."


@pytest.mark.asyncio
async def test_update_profile_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=TenantUserRepository)
    mock_org_repo = mocker.MagicMock(spec=OrganizationRepository)

    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=None)

    new_username = "new"
    updated = mocker.MagicMock()
    updated.username = new_username
    mock_user_repo.update_user = mocker.AsyncMock(return_value=updated)

    service = UserService(user_repository=mock_user_repo, organization_repository=mock_org_repo)

    result = await service.update_profile("tenantZ", old_username="old", new_username=new_username)

    assert result == {"username": new_username}
