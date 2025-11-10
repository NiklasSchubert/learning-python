import json
from os import makedirs, path
from .storage_base import TodoStorage
from todo_item import TodoItem

class JsonTodoStorage(TodoStorage):
    def __init__(self, location: str) -> None:
        super().__init__(location)
        self.STORAGE_FILE = f"{self.LOCATION}/storage.json"

    def loadTodos(self) -> list[TodoItem]:
        if not path.exists(self.STORAGE_FILE):
            return []
        with open(self.STORAGE_FILE) as file:
            return [TodoItem(**data) for data in json.load(file)]

    def writeTodos(self, todos: list[TodoItem]) -> None:
        makedirs(path.dirname(self.STORAGE_FILE), exist_ok=True)
        with open(self.STORAGE_FILE, "w") as file:
            json.dump([t.__dict__ for t in todos], file, indent=2)