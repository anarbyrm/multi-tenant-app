from typing import Optional

from fastapi import Depends

from app.api.requests.login import LoginRequest
from app.api.requests.register import RegisterRequest
from app.core.exceptions import AppException
from app.repositories.tenant_user_repository import TenantUserRepository
from app.repositories.user_repository import UserRepository
from app.utils.jwt import generate_jwt
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        tenant_user_repository: TenantUserRepository = Depends()
    ):
        self.user_repository = user_repository
        self.tenant_user_repository = tenant_user_repository

    async def authenticate_user(self, login_request: LoginRequest, tenant_id: Optional[str]):
        if tenant_id:
            user = await self.tenant_user_repository.get_user_by_username(login_request.username, tenant_id)
        else:
            user = await self.user_repository.get_by_username(login_request.username)

        if not user or not verify_password(login_request.password, user.password):
            raise AppException("Invalid credentials.")

        user_data = {
            "user_id": user.id,
            "username": user.username
        }

        token = generate_jwt(user_data)
        user_data.update({"token": token})

        if not tenant_id:
            organizations = []

            for organization in user.organizations:
                organizations.append({
                    "name": organization.name,
                    "tenant_code": str(organization.tenant_code)
                })

            user_data.update({"organizations": organizations})

        return user_data

    async def register_user(self, register_request: RegisterRequest, tenant_id: Optional[str]):
        hashed_password = hash_password(register_request.password)
        user_exist_error = AppException("User already exists.")

        if tenant_id:
            user = await self.tenant_user_repository.get_user_by_username(register_request.username, tenant_id)

            if user:
                raise user_exist_error

            await self.tenant_user_repository.create_user(
                register_request.username,
                hashed_password,
                tenant_id
            )
        else:
            user = await self.user_repository.get_by_username(register_request.username)

            if user:
                raise user_exist_error

            await self.user_repository.create_user(
                register_request.username,
                hashed_password
            )
