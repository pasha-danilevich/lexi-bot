from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from config import config
from db.mongo.models import Word


async def test_connection(client: AsyncIOMotorClient):
    try:
        await client.admin.command('ping')
        logger.success("✅ Успешное подключение к MongoDB!")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")


async def init_mongo():
    client = AsyncIOMotorClient(
        f"mongodb://{config.MONGO_DB_HOST}:{config.MONGO_DB_PORT}"
    )
    await init_beanie(database=client.lexi, document_models=[Word])
    await test_connection(client)
