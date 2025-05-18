from beanie import Document, Indexed


class Word(Document):
    text: Indexed(str)
    translate: str | list[str]
    usage_count: int | None
    part_of_speech: str | None
    audio: str | list[str] | None
    transcription: str | list[str] | None
    synonyms: str | list[str] | None
    antonyms: str | list[str] | None
    image: str | list[str] | None
    usage_exemple: str | list[str] | None

    class Settings:
        name = "words"

    def __str__(self):
        return f'{self.text}, {self.translate}'
