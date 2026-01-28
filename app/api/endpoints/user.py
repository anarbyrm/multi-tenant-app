from fastapi import APIRouter
from fastapi.params import Depends

from app.services.user_service import UserService

router = APIRouter(prefix='/users')

@router.get('/me')
def get_profile(user_service: UserService = Depends()):
    pass

@router.put('/me')
def update_profile(user_service: UserService = Depends()):
    pass
