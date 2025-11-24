from random import sample, shuffle, choice
from typing import TypedDict
from .mode import Mode
from ...word_loader.word import Word

type Grid = list[list[str | None]]


class GridResult(TypedDict):
    words: list[str]
    grid: Grid


class WordGrid:
    _DIRECTIONS: list[tuple[int, int]] = [
        (0, 1),  # →
        (0, -1),  # ←
        (1, 0),  # ↓
        (-1, 0),  # ↑
        (1, 1),  # ↘
        (1, -1),  # ↙
        (-1, 1),  # ↗
        (-1, -1),  # ↖
    ]

    def _expand_grid(self, grid: Grid) -> Grid:
        WIDTH = max(len(row) for row in grid) if grid else 1
        grid.append([None] * WIDTH)
        for row in grid:
            row.append(None)

    def _expand_grid_to(self, grid: Grid, min_rows: int, min_cols: int):
        while len(grid) < min_rows:
            grid.append([None] * (len(grid[0]) if grid else 0))
        for i in range(len(grid)):
            while len(grid[i]) < min_cols:
                grid[i].append(None)

    def _place(
        self,
        grid: Grid,
        word: str,
        r: int,
        c: int,
        dr: int,
        dc: int,
    ):
        for INDEX, CHAR in enumerate(word):
            rr = r + dr * INDEX
            cc = c + dc * INDEX
            grid[rr][cc] = CHAR

    def _place_word(self, grid: Grid, word: str):
        while True:
            directions = self._DIRECTIONS[:]
            shuffle(directions)

            rows = list(range(len(grid)))
            cols = list(range(len(grid[0]) if grid and grid[0] else 0))
            shuffle(rows)
            shuffle(cols)

            for dr, dc in directions:
                for r in rows:
                    for c in cols:
                        coords = [(r + dr * i, c + dc * i) for i in range(len(word))]

                        if any(rr < 0 or cc < 0 for rr, cc in coords):
                            continue

                        is_collision = False
                        for rr, cc in coords:
                            if (
                                rr < len(grid)
                                and cc < len(grid[rr])
                                and grid[rr][cc] is not None
                            ):
                                is_collision = True
                                break
                        if is_collision:
                            continue

                        max_r = max(rr for rr, _ in coords) + 1
                        max_c = max(cc for _, cc in coords) + 1
                        self._expand_grid_to(grid, max_r, max_c)
                        self._place(grid, word, r, c, dr, dc)
                        return

            self._expand_grid(grid)

    def generate_grid(self, words: list[Word], amount: int) -> GridResult:
        CHOSEN_WORDS = [WORD.get("katakana") for WORD in sample(words, amount)]

        GRID: Grid = []
        for WORD in CHOSEN_WORDS:
            self._place_word(GRID, WORD)

        return GridResult(
            grid=[[cell if cell is not None else " " for cell in row] for row in GRID],
            words=CHOSEN_WORDS,
        )

        UNIQUE_LETTERS = {letter for word in words for letter in word.get("katakana")}
        # return [[cell if cell is not None else choice(UNIQUE_LETTERS) for cell in row] for row in GRID]


class WordSearchPuzzle(Mode):
    _GRID = WordGrid()

    def __init__(self, WORDS: list[Word]):
        super().__init__(WORDS)

    def question(self):

        RESULT = self._GRID.generate_grid(self.WORDS, 3)
        for row in RESULT.GRID:
            print(*row, " ")

        ANSWER = ",".join(RESULT.words)
        RESPONSE = input(
            "Which words can you spot? Enter all 3 seperated by commas in english:\n"
        )
        if RESPONSE == ANSWER:
            print("Correct!")
        else:
            print(f"Wrong! The correct answers were: {ANSWER}")
