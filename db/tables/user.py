from tortoise import fields, models

from db.active_manager import ActiveManager
from db.base_mixin import ActualMixin, TimestampMixin
from db.tables import Collection


class User(models.Model, ActualMixin, TimestampMixin):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(
        max_length=64, null=True
    )  # Может быть None для Telegram
    email = fields.CharField(max_length=255, null=True, unique=True)  # Для сайта
    phone = fields.CharField(max_length=20, null=True, unique=True)  # Опционально

    # Аутентификация
    hashed_password = fields.CharField(max_length=255, null=True)  # Только для сайта
    telegram_id = fields.BigIntField(null=True, unique=True)  # ID в Telegram

    collections: fields.ReverseRelation["Collection"]
    user_words: fields.ReverseRelation["UserWord"]

    class Meta:
        manager = ActiveManager()

    def __str__(self):
        return f"User {self.id} ({self.username or self.email or self.telegram_id})"
