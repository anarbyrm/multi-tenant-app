from fastapi import Depends

from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository
