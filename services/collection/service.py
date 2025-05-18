from services.collection.interface import ICollection
from services.collection.schemas import CollectionDTO
from services.user.service import UserScoped


class CollectionService(ICollection, UserScoped):
    async def get_collections(self) -> list[CollectionDTO]:
        user = await self.get_user()
        collections = await user.collections.all()
        collections = [CollectionDTO(**c.__dict__) for c in collections]
        # collections = [CollectionDTO.model_validate(c) for c in collections] # но нужен from_attributes = True в BaseModel class Config

        return collections

    def __str__(self):
        return self.__class__.__name__


async def run():
    from db.database import init_db
    from services.user.schemas import UserIdentifier

    await init_db()
    service = CollectionService(user_identifier=UserIdentifier(telegram_id=850472798))
    print(await service.get_collections())


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
