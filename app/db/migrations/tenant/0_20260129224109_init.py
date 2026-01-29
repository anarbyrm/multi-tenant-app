from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(30) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "tenant_id" UUID NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_users_usernam_500a9d" UNIQUE ("username", "tenant_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
