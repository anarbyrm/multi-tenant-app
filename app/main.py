from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.exceptions import ValidationException
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import RegisterTortoise

from .api.router import router
from .core.database import TORTOISE_ORM_CONFIG
from .core.exceptions import AppException
from .core.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM_CONFIG,
        generate_schemas=False,
        add_exception_handlers=True
    ):
        yield

app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppException)
async def bad_request_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message}
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exc.errors()}
    )


@app.exception_handler(Exception)
async def server_side_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc) if settings.DEBUG else "Internal Server Error"}
    )

app.include_router(router, prefix='/api')
