from fastapi import APIRouter

router = APIRouter(prefix='/organizations')

@router.post('/')
def create_organization():
    pass
