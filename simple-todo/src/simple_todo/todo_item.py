class TodoItem:
    def __init__(self, name: str, completed: bool) -> None:
        self.name = name
        self.completed = completed

    def complete(self) -> None:
        self.completed = True

    def incomplete(self) -> None:
        self.completed = False

    def __str__(self) -> str:
        return f"[{"✓" if self.completed else "x"}] {self.name}"
