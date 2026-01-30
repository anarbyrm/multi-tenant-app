import pytest_asyncio
from starlette.testclient import TestClient
from tortoise import Tortoise

from app.core.database import TORTOISE_ORM_CONFIG
from app.main import app


@pytest_asyncio.fixture
async def setup_db():
    await Tortoise.init(config=TORTOISE_ORM_CONFIG)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


def get_client():
    return TestClient(app)
