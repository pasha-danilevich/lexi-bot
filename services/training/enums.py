from enum import StrEnum


class TrainingType(StrEnum):
    """Типы упражнений в приложении для изучения языков."""

    # IMAGE_MATCH = "image_match"
    CHOICE_QUIZ = "choice_quiz"
    # PUZZLE = "puzzle"
    # LISTENING_TEST = "listening_test"
    WRITE_TRANSLATION = "write_translation"
    # SPEECH_PRACTICE = "speech_practice"

    @property
    def display_name(self) -> str:
        """Человеко-читаемое название."""
        return {
            self.CHOICE_QUIZ: "Тест",
            self.WRITE_TRANSLATION: "Перевод",
        }[self]

    @property
    def get_lvl(self) -> int:
        """Уровень теста"""
        return {
            self.CHOICE_QUIZ: 1,
            self.WRITE_TRANSLATION: 2,
        }[self]
