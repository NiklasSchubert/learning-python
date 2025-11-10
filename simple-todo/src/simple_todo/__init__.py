from os import name, system
from storage.storage_json import JsonTodoStorage
from storage.storage_csv import CsvTodoStorage
from todo_item import TodoItem

OPTIONS = [
    "Show todos",
    "Add Todo",
    "Remove Todo",
    "Mark as complete",
    "Mark as incomplete",
    "Exit",
]

STORAGE = JsonTodoStorage("./storage")
todos: list[TodoItem] = STORAGE.loadTodos()


def showTodos() -> None:
    print("Action: Show Todos")
    if len(todos) == 0:
        print("No Todos available. Start by creating one.")
    else:
        for INDEX, TODO in enumerate(todos):
            print(f"{INDEX}: {TODO} [{"✓" if TODO.completed else "x"}]")


def addTodo() -> None:
    print("Action: Create Todo")
    NAME: str = input("Enter the name: ")
    todos.append(TodoItem(NAME, False))


def removeTodo() -> None:
    print("Action: Remove Todo")
    showTodos()
    INDEX: int = int(input("Enter the index of the todo: "))
    todos.pop(INDEX)


def markAsComplete() -> None:
    print("Action: Mark as Complete")
    showTodos()
    INDEX = int(input("Which Todo Item has been completed?"))
    todos[INDEX].markCompleted()


def markAsIncomplete() -> None:
    print("Action: Mark as Incomplete")
    showTodos()
    INDEX = int(input("Which Todo Item should be marked incomplete?"))
    todos[INDEX].markIncomplete()


def askOption() -> int:
    for INDEX, OPTION in enumerate(OPTIONS):
        print(f"{INDEX}: {OPTION}")
    return int(input("Choose an options: "))


while True:
    RESPONSE = askOption()
    system("cls" if name == "nt" else "clear")

    if RESPONSE == 0:
        showTodos()
    elif RESPONSE == 1:
        addTodo()
    elif RESPONSE == 2:
        removeTodo()
    elif RESPONSE == 3:
        markAsComplete()
    elif RESPONSE == 4:
        markAsIncomplete()
    else:
        STORAGE.writeTodos(todos)
        break
    print("\n")
