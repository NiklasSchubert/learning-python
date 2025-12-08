from abc import ABC, abstractmethod
from .word import Word


class WordLoader(ABC):
    @abstractmethod
    def load(self) -> list[Word]:
        pass
