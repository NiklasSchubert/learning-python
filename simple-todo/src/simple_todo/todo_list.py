from storage.storage_base import TodoStorage
from todo_item import TodoItem
from typing import Iterator


class TodoList:
    _todos: list[TodoItem] = []

    def __init__(self, storage: TodoStorage):
        self.STORAGE = storage
        self._readStorage()

    def _readStorage(self) -> None:
        self._todos = self.STORAGE.loadTodos()

    def writeStorage(self) -> None:
        self.STORAGE.writeTodos(self._todos)

    def items(self) -> Iterator[TodoItem]:
        return iter(self._todos)

    def getItem(self, INDEX: int) -> TodoItem:
        return self._todos[INDEX]

    def addItem(self, todoItem: TodoItem) -> None:
        self._todos.append(todoItem)

    def removeItem(self, id: int) -> None:
        self._todos.pop(id)
