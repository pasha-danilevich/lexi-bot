from tortoise.expressions import Q
from tortoise.manager import Manager


class ActiveManager(Manager):
    def get_queryset(self):
        return (
            super(ActiveManager, self)
            .get_queryset()
            .filter(Q(active=True, deleted=False, join_type='AND'))
        )
