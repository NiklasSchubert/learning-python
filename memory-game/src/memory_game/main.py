from random import sample, shuffle
import string
from time import sleep
from typing import Generator


class GRID_ITEM:
    def __init__(self, VALUE: str, SOLVED: bool, SHOW: bool) -> None:
        self._VALUE = VALUE
        self._solved = SOLVED
        self._show = SHOW

    def solve(self):
        self._solved = True

    def reveal(self):
        self._solved = True

    def hide(self):
        self._solved = False

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GRID_ITEM):
            return NotImplemented

        return self._VALUE == value._VALUE

    def __str__(self) -> str:
        return self._VALUE if self._solved or self._show else f"-({self._VALUE})"


type MEMORY_GRID = list[list[GRID_ITEM]]


class Game:
    def __init__(self) -> None:
        pass

    def _get_letters(self, AMOUNT: int) -> Generator[str]:
        LETTERS = sample(string.ascii_uppercase, AMOUNT) * 2
        shuffle(LETTERS)
        for LETTER in LETTERS:
            yield LETTER

    def _generate_grid(self, SIZE: int) -> MEMORY_GRID:
        if SIZE % 2 != 0:
            raise ValueError("Size has to be even value")

        NEEDED_PAIRS = int(SIZE**2 / 2)
        LETTER_GEN = self._get_letters(NEEDED_PAIRS)

        GRID = [
            [GRID_ITEM(next(LETTER_GEN), False, False) for _ in range(SIZE)]
            for _ in range(SIZE)
        ]
        return GRID

    def _print_grid(self, GRID: MEMORY_GRID) -> None:
        for ROW in GRID:
            print(" ".join([str(COL) for COL in ROW]))

    def start(self, SIZE: int) -> None:
        GRID = self._generate_grid(SIZE)

        while True:
            for ROW in GRID:
                for COL in ROW:
                    COL.hide()

            self._print_grid(GRID)

            answer = input("Enter a 2 coordinate to try a reveal (e.g.: x,y x,y)")

            COORD_STR_1, COORD_STR_2 = answer.split(" ")
            X1, Y1 = [int(digit) for digit in COORD_STR_1.split(",")[:2]]
            CELL1 = GRID[Y1 - 1][X1 - 1]
            X2, Y2 = [int(digit) for digit in COORD_STR_2.split(",")[:2]]
            CELL2 = GRID[Y2 - 1][X2 - 1]

            CELL1.reveal()
            CELL2.reveal()

            if CELL1 == CELL2:
                print("You found a pair")
                CELL1.solve()
                CELL2.solve()

            self._print_grid(GRID)

            input("Press any key to continue...")


def main():
    Game().start(6)


if __name__ == "__main__":
    main()
