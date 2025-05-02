import os
import shutil

from aerich import Command, models
from tortoise import Tortoise, run_async

from config import BASE_PATH
from db.database import TORTOISE_ORM


class MigrateService:
    def __init__(self, db_config: dict, save: bool = True):
        self.db_config = db_config
        self.save = save

        self._command = Command(
            tortoise_config=self.db_config,
            app='models',
            location=os.path.join(BASE_PATH, "db", 'migrations'),
        )

    async def create_db(self):
        await Tortoise.init(config=self.db_config, _create_db=True)

    async def migrate(self, name):
        try:
            await self._command.init()
            db = await self._command.inspectdb()
            print(db)
        except Exception as e:
            print(e)
        try:
            await self._command.init_db(safe=self.save)
        except Exception as e:
            print(e)
        await self._command.init()
        await self._command.migrate(name=name)
        await self._command.upgrade(run_in_transaction=True)
        return await self._command.history()

    async def downgrade(self, name):
        try:
            await self._command.init()
            await self._command.downgrade(version=name, delete=True)
            return await self._command.history()
        except Exception as e:
            return str(e)

    async def migrate_history(self):
        try:
            await self._command.init()
            return await self._command.history()
        except Exception as e:
            return str(e)

    async def drop_database(self):
        await Tortoise.init(config=self.db_config)
        await Tortoise._drop_databases()

    async def drop_aerich_data(self):
        await Tortoise.init(config=self.db_config)
        aerich_datas = await models.Aerich.all()
        for aerich_data in aerich_datas:
            await aerich_data.delete()
        migrate_folder = os.path.join(BASE_PATH, 'migrations')
        if os.path.isdir(migrate_folder):
            shutil.rmtree(path=migrate_folder)
            print('migrate folder deleted')
        return aerich_datas


async def start():
    service = MigrateService(db_config=TORTOISE_ORM)
    try:
        # await service.drop_database()
        await service.create_db()
    except:
        pass
    await service.migrate('init')


run_async(start())
