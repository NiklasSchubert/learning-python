from abc import ABC, abstractmethod
from todo_item import TodoItem

class TodoStorage(ABC):
    def __init__(self, location: str) -> None:
        self.LOCATION = location

    @abstractmethod
    def loadTodos(self) -> list[TodoItem]:
        pass

    @abstractmethod
    def writeTodos(self, todos: list[TodoItem]) -> None:
        pass
