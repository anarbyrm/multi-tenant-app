from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from .api.router import router
from .core.database import TORTOISE_ORM_CONFIG


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

app.include_router(router, prefix='/api')
