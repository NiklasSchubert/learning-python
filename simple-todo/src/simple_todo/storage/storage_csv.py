from csv import DictReader
from os import makedirs, path
from .storage_base import TodoStorage
from todo_item import TodoItem
from os import path

class CsvTodoStorage(TodoStorage):
    def __init__(self, location: str) -> None:
        super().__init__(location) 
        self.STORAGE_FILE = f"{self.LOCATION}/storage.csv"

    def loadTodos(self) -> list[TodoItem]:
        if not path.exists(self.STORAGE_FILE):
            return []
        with open(self.STORAGE_FILE) as file:
            reader = DictReader(file)
            todos: list[TodoItem] = []
            for ROW in reader:
                NAME = ROW["name"]
                COMPLETED = ROW["completed"]
                todos.append(TodoItem(NAME, COMPLETED))
            return todos

    def writeTodos(self, todos: list[TodoItem]):
        if len(todos) == 0:
            return
        makedirs(path.dirname(self.STORAGE_FILE), exist_ok=True)
        with open(self.STORAGE_FILE, "w") as FILE:
            HEADERS = todos[0].__dict__.keys()
            FILE.write(",".join(HEADERS) + "\n")

            for TODO in todos:
                ROW = [str(value) for value in TODO.__dict__.values()]
                FILE.write(",".join(ROW) + "\n")
