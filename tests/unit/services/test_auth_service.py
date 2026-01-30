import pytest
from app.core.exceptions import AppException
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.tenant_user_repository import TenantUserRepository


@pytest.mark.asyncio
async def test_authenticate_user_main_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    username = "test_user"
    user_id = 1
    token = "token123"

    mock_user = mocker.MagicMock()
    mock_user.id = user_id
    mock_user.username = username
    mock_user.password = "hashed"

    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=mock_user)

    mocker.patch("app.services.auth_service.verify_password", return_value=True)
    mocker.patch("app.services.auth_service.generate_jwt", return_value=token)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    login_req = mocker.MagicMock()
    login_req.username = username
    login_req.password = "test_pass"

    result = await service.authenticate_user(login_req, tenant_id=None)

    assert result["user_id"] == user_id
    assert result["username"] == username
    assert result["token"] == token


@pytest.mark.asyncio
async def test_authenticate_user_tenant_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    username = "tenant_user"
    user_id = 2
    token = "token123"

    mock_user = mocker.MagicMock()
    mock_user.id = user_id
    mock_user.username = username
    mock_user.password = "hashed"

    mock_tenant_repo.get_by_username = mocker.AsyncMock(return_value=mock_user)
    mocker.patch("app.services.auth_service.verify_password", return_value=True)
    mocker.patch("app.services.auth_service.generate_jwt", return_value=token)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    login_req = mocker.MagicMock()
    login_req.username = username
    login_req.password = "pwd"

    result = await service.authenticate_user(login_req, tenant_id="tenant_1")

    assert result == {"user_id": user_id, "username": username, "token": token}


@pytest.mark.asyncio
async def test_authenticate_user_invalid_credentials(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    mock_user = mocker.MagicMock()
    mock_user.password = "hashed"

    mock_tenant_repo.get_by_username = mocker.AsyncMock(return_value=mock_user)
    mocker.patch("app.services.auth_service.verify_password", return_value=False)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    login_req = mocker.MagicMock()
    login_req.username = "u"
    login_req.password = "bad"

    with pytest.raises(AppException) as exc:
        await service.authenticate_user(login_req, tenant_id="t")

    assert str(exc.value) == "Invalid credentials."


@pytest.mark.asyncio
async def test_register_user_main_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    username = "new_test_user"
    hashed_password = "hashed"

    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=None)
    mock_user_repo.create_user = mocker.AsyncMock()
    mocker.patch("app.services.auth_service.hash_password", return_value=hashed_password)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)


    register_req = mocker.MagicMock()
    register_req.username = username
    register_req.password = "password123"

    await service.register_user(register_req, tenant_id=None)

    mock_user_repo.create_user.assert_awaited_once_with(username, hashed_password)


@pytest.mark.asyncio
async def test_register_user_main_user_exists(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    mock_existing = mocker.MagicMock()
    mock_user_repo.get_by_username = mocker.AsyncMock(return_value=mock_existing)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    register_req = mocker.MagicMock()
    register_req.username = "exists"
    register_req.password = "password123"

    with pytest.raises(AppException) as exc:
        await service.register_user(register_req, tenant_id=None)

    assert str(exc.value) == "User already exists."


@pytest.mark.asyncio
async def test_register_user_tenant_success(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    username = "tenant_new_user"
    hashed_password = "hashed"
    tenant_id = "tenant_test"

    mock_tenant_repo.get_by_username = mocker.AsyncMock(return_value=None)
    mock_tenant_repo.create_user = mocker.AsyncMock()
    mocker.patch("app.services.auth_service.hash_password", return_value=hashed_password)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    register_req = mocker.MagicMock()
    register_req.username = username
    register_req.password = "password123"

    await service.register_user(register_req, tenant_id=tenant_id)

    mock_tenant_repo.create_user.assert_awaited_once_with(username, hashed_password, tenant_id)


@pytest.mark.asyncio
async def test_register_user_tenant_user_exists(mocker):
    mock_user_repo = mocker.MagicMock(spec=UserRepository)
    mock_tenant_repo = mocker.MagicMock(spec=TenantUserRepository)

    mock_existing = mocker.MagicMock()
    mock_tenant_repo.get_by_username = mocker.AsyncMock(return_value=mock_existing)

    service = AuthService(user_repository=mock_user_repo, tenant_user_repository=mock_tenant_repo)

    register_req = mocker.MagicMock()
    register_req.username = "exists"
    register_req.password = "password123"

    with pytest.raises(AppException) as exc:
        await service.register_user(register_req, tenant_id="tenantX")

    assert str(exc.value) == "User already exists."
