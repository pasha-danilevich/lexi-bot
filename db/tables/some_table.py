from tortoise import fields

from db.active_manager import ActiveManager
from db.base_mixin import BaseTableMixin


class SomeTable(BaseTableMixin):
    id = fields.BigIntField(pk=True)

    class Meta:
        table = ''
        table_description = ''
        manager = ActiveManager()

    def __str__(self):
        return f'<SomeTable: {self.name}>'
