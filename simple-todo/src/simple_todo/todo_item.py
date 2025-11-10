class TodoItem:
    def __init__(self, name: str, completed: bool) -> None:
        self.name = name
        self.completed = completed

    def markCompleted(self):
        self.completed = True

    def markIncomplete(self):
        self.completed = False

    def __str__(self) -> str:
        return self.name
