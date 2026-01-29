from tortoise import models, fields


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=30)
    password = fields.CharField(max_length=255, null=False)
    tenant_id = fields.UUIDField(default=None)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'users'
        unique_together = (("username", "tenant_id"),)
