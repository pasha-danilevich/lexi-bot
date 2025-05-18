from tortoise import fields, models

from db.active_manager import ActiveManager
from db.base_mixin import ActualMixin, TimestampMixin


class Collection(models.Model, ActualMixin, TimestampMixin):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=64)
    description = fields.TextField()

    user = fields.ForeignKeyField("models.User", related_name="collections")

    is_default = fields.BooleanField(default=False)
    is_public = fields.BooleanField(default=False)

    class Meta:
        manager = ActiveManager()

    def __str__(self):
        return f"Collection {self.id} ({self.name})"
