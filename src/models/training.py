from typing import List, Dict, Any


class Word:
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
    def from_json(cls, json_data: Dict[str, Any]) -> "Word":
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
    def __init__(self, word: Word, training: Training) -> None:
        self.word = word
        self.training = training

    @classmethod
    def __from_json(cls, json_data: Dict[str, Any]) -> "BaseTraining":
        word_data = json_data["word"]
        training_data = json_data["training"]

        word = Word.from_json(word_data)
        training = Training.from_json(training_data)

        return cls(word=word, training=training)

    @classmethod
    def make_obj_list(
        cls, json_data: List[Dict[str, Any]]
    ) -> List["BaseTraining"]:
        return [BaseTraining.__from_json(item) for item in json_data]

    def __str__(self) -> str:
        return f"{self.word.text} - {self.word.translation}"


class TrainingManager:
    def __init__(self, objs: List["BaseTraining"]) -> None:
        self.objs = objs
        self.round = 0
        self.length_training = len(objs)

    def get_corrent_training(self) -> BaseTraining | None:
        try:
            corrent_training = self.objs[self.round]
            self.__increment_round()
        except IndexError:
            return None

        return corrent_training

    def get_previous_training(self) -> BaseTraining | None:
        if self.round == 0:
            return None
        else:
            return self.objs[self.round - 1]

    def __increment_round(self):
        self.round += 1
