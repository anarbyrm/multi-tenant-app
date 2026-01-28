from fastapi import APIRouter
from .endpoints import auth, user, organization

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(organization.router)
