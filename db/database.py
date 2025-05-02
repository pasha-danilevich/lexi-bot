from pprint import pprint

from tortoise import Tortoise

from config import config

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": config.DB_HOST,
                "port": config.DB_PORT,
                "user": config.DB_USER,
                "password": config.DB_PASS,
                "database": config.DB_NAME,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "db.tables"],
            "default_connection": "default",
        }
    },
}


async def show_models():
    await Tortoise.init(config=TORTOISE_ORM)
    models = Tortoise.apps.get("models")  # Получаем все модели
    print("Зарегистрированные модели:")
    pprint(list(models.keys()))


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    import asyncio

    asyncio.run(show_models())
