from datetime import datetime, timezone
from typing import Any
from typing import List, Optional

import jwt


class User:
    def __init__(self, user_data):
        self.id: int = user_data[0]
        self.tg_user_id: int = user_data[1]
        self.access_token: str = user_data[
            2
        ]  # Исправлено на правильный индекс для access_token

    def is_correct_access_token(self) -> bool:
        """Проверка JWT access_token на истечение срока."""
        try:
            # Декодируем токен, чтобы получить его payload
            payload = jwt.decode(
                self.access_token, options={"verify_signature": False}
            )  # Не проверяем подпись для проверки срока

            exp = payload.get(
                "exp"
            )  # Получаем время истечения срока действия токена

            if exp is None:
                return False  # Если 'exp' отсутствует,
            # токен считается недействительным

            # Проверяем, не истек ли токен
            expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            return expiration_time > datetime.now(tz=timezone.utc)
        except jwt.ExpiredSignatureError:
            return False  # Токен истек
        except jwt.InvalidTokenError:
            return False  # Неверный токен


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
        )
