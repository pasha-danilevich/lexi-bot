from typing import List, Optional

from aiogram.types import Message


from database import Database
from utils import check_access_token


class User:
    def __init__(self, message: Message):
        from main import db

        self.db = db

        user_data = self.get_user_data_from_db(message)

        if user_data:
            self.id: int = user_data[0]
            self.tg_user_id: int = user_data[1]
            self.access_token: str = user_data[2]
        else:
            return None

    def get_user_data_from_db(self, message: Message):

        user_id = message.from_user.id  # type: ignore
        user_data = self.db.get_user(tg_user_id=user_id)
        return user_data

    def get_access_token(self):
        return self.access_token

    def update_access_token(self, new_access_token: str) -> None:
        self.db.edit_access_token(
            tg_user_id=self.tg_user_id, new_access_token=new_access_token
        )

    def create_new(self, access_token: str) -> None:
        self.db.add_user(
            tg_user_id=self.tg_user_id,
            access_token=access_token,
        )

    def is_correct_access_token(self) -> bool:
        """Проверка JWT access_token на истечение срока."""
        return check_access_token(self.access_token)


class Translation:
    def __init__(
        self,
        pk: int,
        text: str,
        part_of_speech: int,
        gender: Optional[str],
        frequency: int,
    ):
        self.pk = pk
        self.text = text
        self.part_of_speech = part_of_speech
        self.gender = gender
        self.frequency = frequency

    def __repr__(self):
        return f"Translation(pk={self.pk}, text='{self.text}', part_of_speech={self.part_of_speech}, gender='{self.gender}', frequency={self.frequency})"


class Synonym:
    def __init__(
        self,
        pk: int,
        text: str,
        part_of_speech: int,
        gender: Optional[str],
        frequency: int,
    ):
        self.pk = pk
        self.text = text
        self.part_of_speech = part_of_speech
        self.gender = gender
        self.frequency = frequency

    def __repr__(self):
        return f"Synonym(pk={self.pk}, text='{self.text}', part_of_speech={self.part_of_speech}, gender='{self.gender}', frequency={self.frequency})"


class Meaning:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"Meaning(text='{self.text}')"


class Word:
    def __init__(
        self,
        pk: int,
        text: str,
        part_of_speech: str,
        transcription: str,
        translations: List[Translation],
        synonyms: List[Synonym],
        meanings: List[Meaning],
        related_pk: List[int],
    ):
        self.pk = pk
        self.text = text
        self.part_of_speech = part_of_speech
        self.transcription = transcription
        self.translations = translations
        self.synonyms = synonyms
        self.meanings = meanings

        self.related_pk = related_pk

    def get_translation(self, pk: int) -> Translation | None:
        for translation in self.translations:
            if translation.pk == pk:
                return translation

        return None

    @classmethod
    def from_json(cls, json_data):
        word_data = json_data["word"]

        translations = [
            Translation(**translation)
            for translation in word_data["translations"]
        ]

        synonyms = [Synonym(**synonym) for synonym in word_data["synonyms"]]

        meanings = [Meaning(**meaning) for meaning in word_data["meanings"]]

        return cls(
            pk=word_data["pk"],
            text=word_data["text"],
            part_of_speech=word_data["part_of_speech"],
            transcription=word_data["transcription"],
            translations=translations,
            synonyms=synonyms,
            meanings=meanings,
            related_pk=json_data["related_pk"],
        )

    def __repr__(self):
        return (
            f"Word(pk={self.pk}, text='{self.text}', part_of_speech='{self.part_of_speech}', "
            f"transcription='{self.transcription}', translations={self.translations}, "
            f"synonyms={self.synonyms}, meanings={self.meanings})"
            f"reladed_pk={self.related_pk}"
        )
