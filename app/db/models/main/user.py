from tortoise import models, fields


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    password = fields.CharField(max_length=255, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'users'
