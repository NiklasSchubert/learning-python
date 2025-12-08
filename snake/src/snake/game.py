import curses
from random import choice, randint
import time
from snake.constraints import Constraints
from snake.key_listener import KeyListener
from snake.position import Position
from snake.snake import Snake
from snake.direction import Direction


class Game:
    def __init__(self, constraints: Constraints) -> None:
        self._constraints: Constraints = constraints
        self._current_apple: Position = self._spawnApple()
        self._SNAKE: Snake = self._spawnSnake()
        self._KEY_LISTENER = KeyListener()

    async def start(self) -> None:
        WINDOW = curses.initscr()
        WINDOW.keypad(True)
        self._KEY_LISTENER.start(WINDOW)

        INTERVAL: float = 0.3

        while True:
            START_TIME = time.perf_counter()

            self._tick()
            self._draw(WINDOW)

            ELAPSED = time.perf_counter() - START_TIME
            time.sleep(max(0.0, INTERVAL - ELAPSED))

    def _tick(self) -> None:
        if self._current_apple in self._SNAKE.coords():
            self._current_apple = self._spawnApple()
            self._SNAKE.increaseLength()

        QUEUE = self._KEY_LISTENER.queue
        if not QUEUE.empty():
            self._steerSnake(QUEUE.get_nowait())

        self._SNAKE.move(self._constraints)

    def _draw(self, stdscr: curses.window) -> None:
        WIDTH: int = self._constraints.mapWidth
        HEIGHT: int = self._constraints.mapHeight

        stdscr.clear()

        # Draw top border once
        stdscr.addstr(0, 0, "_" * (WIDTH * 2 + 1))

        # Draw the map row by row
        for y in range(HEIGHT):
            ROW: list[str] = []
            for x in range(WIDTH):
                POSITION = Position(x, y)
                if POSITION in self._SNAKE.coords():
                    ROW.append("S")
                elif POSITION == self._current_apple:
                    ROW.append("A")
                else:
                    ROW.append(".")
            stdscr.addstr(y + 1, 0, f"|{" ".join(ROW)}|")

        # Draw bottom border
        stdscr.addstr(HEIGHT + 1, 0, "_" * (WIDTH * 2 + 1))

        # Use noutrefresh + doupdate for smoother redraw
        stdscr.refresh()

    def _steerSnake(self, KEY: int) -> None:
        mapping: dict[int, Direction] = {
            curses.KEY_UP: Direction.UP,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
            curses.KEY_RIGHT: Direction.RIGHT,
        }
        DIRECTION = mapping.get(KEY, None)
        if DIRECTION == None:
            return

        self._SNAKE.setDirection(DIRECTION)

    def _spawnSnake(self) -> Snake:
        X: int = randint(2, self._constraints.mapWidth - 2)
        Y: int = randint(2, self._constraints.mapHeight - 2)
        DIRECTION: Direction = choice(list(Direction))
        return Snake(X, Y, DIRECTION, [])

    def _spawnApple(self) -> Position:
        X: int = randint(0, self._constraints.mapWidth - 1)
        Y: int = randint(0, self._constraints.mapHeight - 1)
        return Position(X, Y)
