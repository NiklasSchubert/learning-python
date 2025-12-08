from abc import ABC, abstractmethod
from ...ui.ui import UI
from ...word_loader.word import Word


class Mode(ABC):
    def __init__(self, UI: UI, WORDS: list[Word]):
        self.WORDS = WORDS
        self.UI = UI

    @abstractmethod
    def start(self) -> None:
        pass
