from tortoise import models, fields


class User(models.Model):
    id = fields.BigIntField(pk=True)
    code = fields.UUIDField(unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'users'
