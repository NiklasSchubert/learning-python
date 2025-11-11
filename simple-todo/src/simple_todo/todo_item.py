class TodoItem:
    def __init__(self, name: str, completed: bool) -> None:
        self.name = name
        self.completed = completed

    def __str__(self) -> str:
        return self.name
