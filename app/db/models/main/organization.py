import uuid

from tortoise import models, fields


class Organization(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField(
        'main.User',
        related_name='organizations',
        on_delete=fields.CASCADE)
    tenant_code = fields.UUIDField(unique=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'organizations'
