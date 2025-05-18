import random
from datetime import datetime, timedelta

from tortoise import Tortoise, run_async

from db.database import init_db
from db.mongo.database import init_mongo
from db.mongo.models import Word
from db.tables import Collection, User, UserWord


async def generate_mock_data():
    print("⏳ Генерация тестовых данных...")

    # 1. Создаем тестового пользователя
    user = await User.create(
        telegram_id=850472798,
    )
    print(f"✅ Создан пользователь: {user}")

    # 2. Создаем коллекции
    collections = []
    for i, name in enumerate(["Основная", "Фразовые глаголы", "IT термины"]):
        collection = await Collection.create(
            id=i + 1,
            name=name,
            description=f"Тестовая коллекция {name.lower()}",
            user=user,
            is_default=(i == 0),
        )
        collections.append(collection)
        print(f"✅ Создана коллекция: {collection.name}")

    # 3. Генерируем слова в MongoDB
    english_words = [
        ("apple", "яблоко"),
        ("home", "дом"),
        ("good", "хорошо"),
        ("run", ["бегать", "запускать"]),
        ("database", "база данных"),
        ("algorithm", "алгоритм"),
        ("interface", "интерфейс"),
    ]

    for word, translate in english_words:
        await Word(
            text=word,
            translate=translate,
            part_of_speech="noun" if random.random() > 0.5 else "verb",
            usage_count=random.randint(0, 100),
            transcription=word.upper(),
            synonyms=["similar"],
            antonyms=["opposite"],
            usage_exemple=f"I use {word} every day",
            audio=None,
            image=None,
        ).insert()
    print(f"✅ Создано {len(english_words)} слов в MongoDB")

    # 4. Создаем UserWords (связи пользователя со словами)
    words = await Word.find_all().to_list()
    review_dates = [datetime.now().date() + timedelta(days=i) for i in range(5)]

    for i, word in enumerate(words):
        user_word = await UserWord.create(
            id=i + 1,
            word_text=word.text,
            user=user,
            collection=collections[i % len(collections)],
            mongo_id=str(word.id),
            review_level=random.randint(1, 5),
            next_review=random.choice(review_dates),
            associations=f"Ассоциации для {word.text}",
        )
    print(f"✅ Создано {len(words)} связей UserWord")

    print("🎉 Все тестовые данные успешно созданы!")


async def main():
    await init_db()
    await init_mongo()
    await generate_mock_data()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(main())
