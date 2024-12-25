from typing import List, Dict, Any


class TrainingWord:
    def __init__(
        self,
        text: str,
        translation: str,
        transcription: str,
        part_of_speech: str,
    ) -> None:
        self.text = text
        self.translation = translation
        self.transcription = transcription
        self.part_of_speech = part_of_speech

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "TrainingWord":
        return cls(
            text=json_data["text"],
            translation=json_data["translation"],
            transcription=json_data["transcription"],
            part_of_speech=json_data["part_of_speech"],
        )


class Training:
    def __init__(self, pk: int, lvl: int) -> None:
        self.pk = pk
        self.lvl = lvl

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Training":
        return cls(pk=json_data["pk"], lvl=json_data["lvl"])


class FalseSet: ...


class BaseTraining:
    def __init__(self, word: TrainingWord, training: Training) -> None:
        self.word = word
        self.training = training

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "BaseTraining":
        word_data = json_data["word"]
        training_data = json_data["training"]

        word = TrainingWord.from_json(word_data)
        training = Training.from_json(training_data)

        return cls(word=word, training=training)


# Пример использования
def parse_json_data(json_data: List[Dict[str, Any]]) -> List[BaseTraining]:
    return [BaseTraining.from_json(item) for item in json_data]


# Пример данных
json_data = [
    {
        "word": {
            "text": "grounds",
            "translation": "прилегающая территория",
            "transcription": "graʊndz",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1104, "lvl": 1},
    },
    {
        "word": {
            "text": "though",
            "translation": "однако",
            "transcription": "ðəʊ",
            "part_of_speech": "союз",
        },
        "training": {"pk": 802, "lvl": 2},
    },
    {
        "word": {
            "text": "room",
            "translation": "номер",
            "transcription": "rum",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1698, "lvl": 2},
    },
    {
        "word": {
            "text": "room",
            "translation": "возможности",
            "transcription": "rum",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1054, "lvl": 1},
    },
    {
        "word": {
            "text": "tamarisk",
            "translation": "гребенщик",
            "transcription": "ˈtæmərɪsk",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1894, "lvl": 1},
    },
    {
        "word": {
            "text": "into",
            "translation": "внутрь",
            "transcription": "ˈɪntuː",
            "part_of_speech": "предл",
        },
        "training": {"pk": 1546, "lvl": 2},
    },
    {
        "word": {
            "text": "pasha",
            "translation": "паша",
            "transcription": "ˈpɑːʃə",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1364, "lvl": 2},
    },
    {
        "word": {
            "text": "mir",
            "translation": "мир",
            "transcription": "ˈmɪər",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 798, "lvl": 1},
    },
    {
        "word": {
            "text": "cat",
            "translation": "кошачий",
            "transcription": "kæt",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 1328, "lvl": 2},
    },
    {
        "word": {
            "text": "card",
            "translation": "перфокарта",
            "transcription": "kɑːd",
            "part_of_speech": "сущ",
        },
        "training": {"pk": 832, "lvl": 2},
    },
]

# Парсинг данных
base_trainings = parse_json_data(json_data)

# Проверка результата
for base_training in base_trainings:
    print(
        f"Word: {base_training.word.text}, Translation: {base_training.word.translation}, Level: {base_training.training.lvl}"
    )
