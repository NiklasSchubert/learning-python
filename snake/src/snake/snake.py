from snake.constraints import Constraints
from snake.direction import Direction
from snake.position import Position


class Snake:
    def __init__(
        self, x: int, y: int, direction: Direction, tail: list[Position]
    ) -> None:
        self._x = x
        self._y = y
        self._direction = direction
        self._tail = tail

    def move(self, constraints: Constraints) -> None:
        dx, dy = {
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.UP: (0, -1),
        }[self._direction]

        if len(self._tail) > 0:
            NEW_TAIL = Position(self._x, self._y)
            self._tail = [NEW_TAIL, *self._tail[:-1]]

        NEW_X = (self._x + dx) % constraints.mapWidth
        NEW_Y = (self._y + dy) % constraints.mapHeight

        self._x = NEW_X
        self._y = NEW_Y

    def setDirection(self, direction: Direction) -> None:
        self._direction = direction

    def coords(self) -> tuple[Position, ...]:
        return (Position(self._x, self._y), *self._tail)

    def increaseLength(self) -> None:
        self._tail.append(Position(self._x, self._y))

    def __str__(self) -> str:
        return f"Snake(X={self._x}, Y={self._y}, DIRECTION={self._direction})"
