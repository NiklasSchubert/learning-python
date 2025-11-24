from abc import ABC, abstractmethod


class UI(ABC):
    @abstractmethod
    def ask_option(self, question: str, options: dict[int, str]) -> int:
        pass
