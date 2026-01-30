import uuid

import pytest

from app.db.models.main import Organization

from app.db.models.main import User as MainUser
from app.db.models.tenant import User as TenantUser
from app.utils.jwt import generate_jwt
from app.utils.password import hash_password
from .setup import setup_db, get_client


@pytest.mark.asyncio
async def test_main_user_can_register(setup_db):
    client = get_client()
    username = 'testing1234'

    response = client.post('/api/auth/register', json={
        'username': username,
        'password': 'password',
    })

    assert response.status_code == 201

    user = await MainUser.get_or_none(username=username)

    assert user


@pytest.mark.asyncio
async def test_main_user_can_login(setup_db):
    client = get_client()

    password = 'password'
    username = 'testing1234'
    hashed_password = hash_password(password)
    user = await MainUser.create(username=username, password=hashed_password)

    response = client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })

    assert response.status_code == 200
    data = response.json()
    assert user.id == data['user_id']
    assert user.username == data['username']


@pytest.mark.asyncio
async def test_tenant_user_can_register(setup_db):
    client = get_client()
    tenant_id = str(uuid.uuid4())
    username = 'main_user'
    password = 'main_user_pass'

    user = await MainUser.create(username=username, password=password)
    await Organization.create(name='org', user=user, tenant_code=tenant_id)

    token = generate_jwt({
        "user_id": user.id,
        "username": user.username
    })

    client.headers = {
        "X-TENANT": tenant_id,
        "Authorization": f"Bearer {token}"
    }

    tenant_username = 'tenant_user'
    tenant_password = 'tenant_user_pass'

    response = client.post('/api/auth/register', json={
        'username': tenant_username,
        'password': tenant_password,
    })

    assert response.status_code == 201

    user = await TenantUser.get_or_none(tenant_id=tenant_id, username=tenant_username)

    assert user


@pytest.mark.asyncio
async def test_tenant_user_can_login(setup_db):
    client = get_client()
    tenant_id = str(uuid.uuid4())
    username = 'main_user'
    password = 'main_user_pass'
    tenant_username = 'tenant_user'
    tenant_password = 'tenant_user_pass'

    user = await MainUser.create(username=username, password=password)
    await Organization.create(name='org', user=user, tenant_code=tenant_id)
    tenant_user = await TenantUser.create(username=tenant_username, password=hash_password(tenant_password), tenant_id=tenant_id)

    token = generate_jwt({
        "user_id": user.id,
        "username": user.username
    })

    client.headers = {
        "X-TENANT": tenant_id,
        "Authorization": f"Bearer {token}"
    }

    response = client.post('/api/auth/login', json={
        'username': tenant_username,
        'password': tenant_password,
    })

    assert response.status_code == 200
    data = response.json()
    assert tenant_user.id == data['user_id']
    assert tenant_user.username == data['username']
