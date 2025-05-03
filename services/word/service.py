from mock.word.service import WordMockService


class WordService(WordMockService):
    def __str__(self):
        return self.__class__.__name__
