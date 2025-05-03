from faker import Faker

from services.collection.interface import ICollection
from services.collection.schemas import Collection
from services.user.service import UserScoped

fake = Faker(locale='ru')


class CollectionMockService(ICollection, UserScoped):
    async def get_collections(self) -> list[Collection]:
        user = self.user
        collections_fake = [
            Collection(
                id=fake.random_int(), name=f'{fake.word().title()} {fake.word()}'
            )
            for _ in range(10)
        ]
        return collections_fake
