from typing import Any, Dict, List, Optional

from tortoise.exceptions import DoesNotExist
from tortoise.models import Model


class CRUDMixin:
    @classmethod
    async def create(cls, **kwargs) -> Model:
        return await cls.create(**kwargs)

    async def update(self, **kwargs) -> None:
        await self.update_from_dict(kwargs).save()

    async def delete(self) -> None:
        await self.delete()

    @classmethod
    async def get(cls, *args, **kwargs) -> Optional[Model]:
        try:
            return await cls.get(*args, **kwargs)
        except DoesNotExist:
            return None

    @classmethod
    async def get_all(
        cls,
        filters: Optional[Dict[str, Any]] = None,
        ordering: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[Model]:
        query = cls.all()
        if filters:
            query = query.filter(**filters)
        if ordering:
            query = query.order_by(*ordering)
        if limit:
            query = query.limit(limit)
        return await query

    @classmethod
    async def get_or_create(
        cls, defaults: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Model:
        return await cls.get_or_create(defaults=defaults, **kwargs)
