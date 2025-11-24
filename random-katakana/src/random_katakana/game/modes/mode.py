from abc import ABC, abstractmethod
from ...word_loader.word import Word


class Mode(ABC):
    def __init__(self, WORDS: list[Word]):
        self.WORDS = WORDS

    @abstractmethod
    def question(self):
        pass
