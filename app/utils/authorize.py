from typing import Optional

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.repositories.tenant_user_repository import TenantUserRepository
from app.repositories.user_repository import UserRepository
from app.utils.jwt import verify_jwt

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repo: UserRepository = Depends(),
) -> dict:
    token = credentials.credentials
    payload = verify_jwt(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = await user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return {
        "user_id": user.id,
        "username": user.username,
        "organizations": user.organizations
    }


async def authorize_current_tenant(
    tenant_id: Optional[str] = Header(default=None, alias="X-TENANT"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    user_repo: UserRepository = Depends()
):
    if not tenant_id:
        return

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for tenant access",
        )

    user = await get_current_user(credentials, user_repo)

    for organization in user["organizations"]:
        if str(organization.tenant_code) == tenant_id:
            return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not authorized for this tenant",
    )


async def get_current_tenant_user(
    tenant_id: str = Header(..., alias="X-TENANT"),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repo: TenantUserRepository = Depends(),
):
    token = credentials.credentials
    payload = verify_jwt(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = await user_repo.get_by_id(user_id, tenant_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant user not found",
        )

    return {
        "user_id": user.id,
        "username": user.username,
    }
