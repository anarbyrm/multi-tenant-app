from datetime import datetime, timedelta

from jose import jwt

from app.core.settings import get_settings

settings = get_settings()


def generate_jwt(data: dict):
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    data.update({"exp": expire})

    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_jwt(token: str):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
