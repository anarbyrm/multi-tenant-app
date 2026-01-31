# **Project: Multi-tenant FastAPI service with Tortoise ORM**

## **Overview**
- A FastAPI application that supports both main and tenant-scoped users and organizations.
- Uses Tortoise ORM with Aerich for migrations and PostgreSQL for persistence.
- JWT-based authentication. Tenancy is indicated via the X-TENANT header.

## **Tech stack**
- Python 3.12
- FastAPI + Uvicorn
- Tortoise ORM + Aerich
- PostgreSQL (two databases: main and tenant)
- Pytest
- Docker and Docker Compose

## **Project layout (key files)**
- app/main.py – FastAPI application and exception handlers
- app/api/endpoints – HTTP endpoints (auth, users, organizations)
- app/core – settings and DB config
- app/db/migrations – Aerich migrations (main and tenant)
- app/services – business logic
- tests – unit and integration tests

## **Environment variables**
Create a .env file in the repository root. Required keys (see app/core/settings.py):
- DEBUG
- POSTGRES_USER
- POSTGRES_PASSWORD
- MAIN_DB_NAME
- TENANT_DB_NAME
- MAIN_DB_URL
- TENANT_DB_URL
- ACCESS_TOKEN_EXPIRE
- SECRET_KEY
- ALGORITHM

Notes:
- When using docker-compose, MAIN_DB_URL and TENANT_DB_URL are overridden to point to the compose services.
- Tests read variables from .env.testing automatically (tests/conftest.py).

## **How to run (Docker)**
1) Build and start all services:

```bash
docker-compose up --build
```

2) The API will be available at:
   http://localhost:8000
   Interactive docs (Swagger UI): http://localhost:8000/docs

### **Docker services/ports**
- db_main: PostgreSQL main DB at localhost:5432
- db_tenant: PostgreSQL tenant DB at localhost:5433
- api: FastAPI at localhost:8000

## **Authentication**
- JWT Bearer tokens are used for protected endpoints.
- Include the header: Authorization: Bearer <token>
- Tenancy-sensitive endpoints additionally require the header: X-TENANT: <tenant_code>

## **Simple API paths**
- POST /api/auth/login — Authenticate a user; add X-TENANT to log into tenant space.
- POST /api/auth/register — Register a new user; optional X-TENANT for tenant scope.
- POST /api/organizations/ — Create an organization (requires Authorization).
- GET /api/users/me — Get a current tenant user profile (requires X-TENANT and Authorization).
- PATCH /api/users/me — Update a current tenant user profile (requires X-TENANT and Authorization).

## **Running tests**
- Unit and integration tests are under tests/.
- Tests autoload environment from .env.testing (see tests/conftest.py).

Run all tests:

```bash
pytest
```

Run only unit tests:

```bash
pytest tests/unit
```

Run only integration tests:

```bash
pytest tests/integration
```
