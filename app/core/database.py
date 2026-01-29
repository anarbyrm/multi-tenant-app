from .settings import get_settings

settings = get_settings()

TORTOISE_ORM_CONFIG = {
    "connections": {
        "main": str(settings.MAIN_DB_URL),
        "tenant": str(settings.TENANT_DB_URL),
    },
    "apps": {
        "main": {
            "models": ["app.db.models.main", "aerich.models"],
            "default_connection": "main",
        },
        "tenant": {
            "models": ["app.db.models.tenant", "aerich.models"],
            "default_connection": "tenant",
        },
    },
}
