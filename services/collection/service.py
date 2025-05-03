from mock.collection.service import CollectionMockService


class CollectionService(CollectionMockService):
    def __str__(self):
        return self.__class__.__name__
