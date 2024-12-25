from typing import List, Optional


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
