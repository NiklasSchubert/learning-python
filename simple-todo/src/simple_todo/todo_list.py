from storage.storage_json import JsonTodoStorage
from todo_item import TodoItem


class TodoList:
    _todos: list[TodoItem] = []
    STORAGE = JsonTodoStorage("./storage")

    def __init__(self):
        self._readStorage()

    def _readStorage(self) -> None:
        self._todos = self.STORAGE.loadTodos()

    def writeStorage(self) -> None:
        self.STORAGE.writeTodos(self._todos)

    def items(self) -> tuple[TodoItem, ...]:
        return tuple(self._todos)

    def addTodoItem(self, todoItem: TodoItem) -> None:
        self._todos.append(todoItem)

    def removeTodoItem(self, id: int) -> None:
        self._todos.pop(id)

    def updateTodoItem(self, id: int, todoItem: TodoItem) -> None:
        self._todos[id] = todoItem

    def markAsComplete(self, id: int) -> None:
        CURRENT_ITEM = self.items()[id]
        CURRENT_ITEM.completed = True

    def markAsIncomplete(self, id: int) -> None:
        CURRENT_ITEM = self.items()[id]
        CURRENT_ITEM.completed = False
