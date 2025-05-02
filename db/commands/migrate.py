import asyncio
from pathlib import Path

from aerich import Command

from config import BASE_PATH
from db.database import TORTOISE_ORM


async def migrate():
    # Инициализация Aerich
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app="models",
        location=str(Path(BASE_PATH, 'db', 'migrations')),
    )

    await command.init()
    await command.init_db(safe=True)
    await command.migrate()
    await command.upgrade()


if __name__ == "__main__":
    asyncio.run(migrate())
