import asyncio
from snake.direction import Direction
from snake.game import Constraints, Game
from snake.snake import Snake


def main():
    constraints = Constraints(10, 10, True)
    asyncio.run(Game(constraints).start())


if __name__ == "__main__":
    main()
