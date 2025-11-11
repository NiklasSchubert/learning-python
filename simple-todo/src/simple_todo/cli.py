from enum import Enum, auto
from os import name, system
from typing import Callable
from todo_list import TodoList
from todo_item import TodoItem


class Option(Enum):
    SHOW_TODOS = auto()
    ADD_TODO = auto()
    REMOVE_TODO = auto()
    MARK_AS_COMPLETE = auto()
    MARK_AS_INCOMPLETE = auto()
    EXIT = auto()


TODO_LIST = TodoList()


def showTodos() -> None:
    print("Action: Show Todos")
    if len(TODO_LIST.items()) == 0:
        print("No Todos available. Start by creating one.")
    else:
        for INDEX, TODO in enumerate(TODO_LIST.items()):
            print(f"{INDEX}: {TODO} [{"✓" if TODO.completed else "x"}]")


def addTodo() -> None:
    print("Action: Create Todo")
    NAME: str = input("Enter the name: ")
    TODO_ITEM = TodoItem(NAME, False)
    TODO_LIST.addTodoItem(TODO_ITEM)


def removeTodo() -> None:
    print("Action: Remove Todo")
    showTodos()
    INDEX: int = int(input("Enter the index of the todo: "))
    TODO_LIST.removeTodoItem(INDEX)


def markAsComplete() -> None:
    print("Action: Mark as Complete")
    showTodos()
    INDEX = int(input("Which Todo Item has been completed?"))
    TODO_LIST.markAsComplete(INDEX)


def markAsIncomplete() -> None:
    print("Action: Mark as Incomplete")
    showTodos()
    INDEX = int(input("Which Todo Item should be marked incomplete?"))
    TODO_LIST.markAsIncomplete(INDEX)


def exit() -> bool:
    TODO_LIST.writeStorage()
    return True


OPTION_FUNCTION_MAP: dict[Option, Callable[[], None | bool]] = {
    Option.SHOW_TODOS: showTodos,
    Option.ADD_TODO: addTodo,
    Option.REMOVE_TODO: removeTodo,
    Option.MARK_AS_COMPLETE: markAsComplete,
    Option.MARK_AS_INCOMPLETE: markAsIncomplete,
    Option.EXIT: exit,
}


def askOption() -> Option | None:
    for OPTION in Option:
        print(f"{OPTION.value}: {OPTION.name}")

    try:
        SELECTED_OPTION = int(input("Choose an options: "))
        return Option(SELECTED_OPTION)
    except ValueError:
        return None


def startCli() -> None:
    while True:
        RESPONSE = askOption()
        system("cls" if name == "nt" else "clear")

        if RESPONSE == None:
            print("Invalid option \n")
            continue

        EXIT = OPTION_FUNCTION_MAP[RESPONSE]()
        if EXIT:
            break

        print("\n")
