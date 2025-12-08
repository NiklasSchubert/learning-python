from abc import ABC, abstractmethod


class UI(ABC):
    @abstractmethod
    def ask_option(self, question: str, options: dict[int, str]) -> int:
        pass

    @abstractmethod
    def show_text(self, text: str) -> None:
        pass

    @abstractmethod
    def request_input(self, text: str) -> str:
        pass

    @abstractmethod
    def show_error(self, text: str) -> None:
        pass
