from tortoise import fields, models
from tortoise.validators import MinValueValidator

from db.base_mixin import TimestampMixin


class UserWord(models.Model, TimestampMixin):
    id = fields.BigIntField(pk=True)
    word_text = fields.CharField(max_length=128, unique=True)

    associations = fields.CharField(max_length=500, null=True)
    review_level = fields.IntField(
        default=1, validators=[MinValueValidator(1)], description="Уровень слова"
    )
    next_review = fields.DateField(description="Дата следующего повторения")

    mongo_id = fields.CharField(
        max_length=24, description="Внешний ключ на коллекцию в Mongo"
    )
    collection = fields.ForeignKeyField(
        "models.Collection", related_name="words", on_delete=fields.CASCADE, index=True
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="user_words", on_delete=fields.CASCADE, index=True
    )

    class Meta:
        table = "user_word"
        unique_together = [("id", "word_text")]
        indexes = [("user_id", "next_review"), ("user_id", "review_level")]

    def __str__(self):
        return f"word: {self.word_text} in {self.collection.name} collection"
