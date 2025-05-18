from pprint import pprint

from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

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
    logger.success("Зарегистрированные модели:")
    pprint(list(models.keys()))


async def ping_db():
    """
    Проверяет подключение к базе данных через Tortoise ORM
    """
    try:
        conn = Tortoise.get_connection("default")
        await conn.execute_query("SELECT 1")
        logger.success("✅ Успешное подключение к PostgreSQL через Tortoise ORM!")
        return True
    except DBConnectionError as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}")
        return False


async def init_db():
    """
    Инициализация БД с проверкой подключения
    """

    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await ping_db()
        await Tortoise.generate_schemas()
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации Tortoise ORM: {e}")
        raise


if __name__ == '__main__':
    import asyncio

    asyncio.run(show_models())
