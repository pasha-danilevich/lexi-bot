from typing import Any

from tortoise import fields, models


class BaseDBModel(models.Model):
    async def to_dict(
        self, exclude: set[str] = None, prefetch: bool = False
    ) -> dict[str, Any]:
        d = {}
        db_fields = self._meta.db_fields

        if exclude is not None:
            db_fields = db_fields - exclude

        for field in db_fields:
            d[field] = getattr(self, field)

        if prefetch:
            for field in self._meta.backward_fk_fields:
                d[field] = await getattr(self, field).all().values()

        return d

    class Meta:
        abstract = True


class ActualMixin:
    active = fields.BooleanField(default=True)
    deleted = fields.BooleanField(default=False)


class TimestampMixin:
    """
    Миксин для автоматического управления датами создания и обновления
    """

    created_at = fields.DatetimeField(
        auto_now_add=True, description="Дата и время создания записи", null=False
    )
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="Дата и время последнего обновления записи",
        null=False,
    )


class BaseTableMixin(BaseDBModel, TimestampMixin, ActualMixin):
    pass
