from enum import Enum, auto
from os import name, system
from typing import Callable
from storage.storage_json import JsonTodoStorage
from todo_list import TodoList
from todo_item import TodoItem


class CliOption(Enum):
    SHOW_TODOS = auto()
    ADD_TODO = auto()
    REMOVE_TODO = auto()
    MARK_AS_COMPLETE = auto()
    MARK_AS_INCOMPLETE = auto()
    EXIT = auto()


class Cli:
    _TODO_LIST = TodoList(JsonTodoStorage("./storage"))

    def _callFunction(self, option: CliOption) -> None | bool:
        FUNCTION_MAP: dict[CliOption, Callable[[], None | bool]] = {
            CliOption.SHOW_TODOS: self._showTodos,
            CliOption.ADD_TODO: self._addTodo,
            CliOption.REMOVE_TODO: self._removeTodo,
            CliOption.MARK_AS_COMPLETE: self._markAsComplete,
            CliOption.MARK_AS_INCOMPLETE: self._markAsIncomplete,
            CliOption.EXIT: self._exit,
        }

        return FUNCTION_MAP[option]()

    def _showTodos(self) -> None:
        print("Action: Show Todos")
        empty = True
        for INDEX, TODO in enumerate(self._TODO_LIST.items()):
            empty = False
            print(f"{INDEX}: {TODO}")
        if empty:
            print("No Todos available. Start by creating one.")

    def _addTodo(self) -> None:
        print("Action: Create Todo")
        NAME: str = input("Enter the name: ")
        TODO_ITEM = TodoItem(NAME, False)
        self._TODO_LIST.addItem(TODO_ITEM)

    def _removeTodo(self) -> None:
        print("Action: Remove Todo")
        self._showTodos()
        INDEX: int = int(input("Enter the index of the todo: "))
        self._TODO_LIST.removeItem(INDEX)

    def _markAsComplete(self) -> None:
        print("Action: Mark as Complete")
        self._showTodos()
        INDEX: int = int(input("Which Todo Item has been completed?"))
        self._TODO_LIST.getItem(INDEX).complete()

    def _markAsIncomplete(self) -> None:
        print("Action: Mark as Incomplete")
        self._showTodos()
        INDEX: int = int(input("Which Todo Item should be marked incomplete?"))
        self._TODO_LIST.getItem(INDEX).incomplete()

    def _exit(self) -> bool:
        self._TODO_LIST.writeStorage()
        return True

    def _askOption(self) -> CliOption | None:
        for OPTION in CliOption:
            print(f"{OPTION.value}: {OPTION.name}")

        try:
            SELECTED_OPTION = int(input("Choose an options: "))
            return CliOption(SELECTED_OPTION)
        except ValueError:
            return None

    def start(self) -> None:
        while True:
            RESPONSE = self._askOption()
            system("cls" if name == "nt" else "clear")

            if RESPONSE == None:
                print("Invalid option \n")
                continue

            EXIT = self._callFunction(RESPONSE)
            if EXIT:
                break

            print("\n")
