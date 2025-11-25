from collections import Counter
from random import sample, shuffle, choice
from typing import TypedDict
from .mode import Mode
from ...word_loader.word import Word

type Grid = list[list[str | None]]
type FilledGrid = list[list[str]]


class GridResult(TypedDict):
    words: list[str]
    grid: FilledGrid


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
        width = max((len(row) for row in grid), default=1)
        # existing rows get one appended None; add a new row of length (width + 1)
        new_rows = [row[:] + [None] for row in grid]
        new_rows.append([None] * (width + 1))
        return new_rows

    def _expand_grid_to(self, GRID: Grid, MINIMUM_ROWS: int, MINIMUM_COLS: int) -> Grid:
        CURRENT_ROWS = len(GRID)
        CURRENT_COLS = len(GRID[0]) if GRID and GRID[0] else 0
        TARGET_ROWS = max(CURRENT_ROWS, MINIMUM_ROWS)
        TARGET_COLS = max(CURRENT_COLS, MINIMUM_COLS)

        new_grid: Grid = []
        for INDEX in range(TARGET_ROWS):
            if INDEX < CURRENT_ROWS:
                row = GRID[INDEX][:]
                if len(row) < TARGET_COLS:
                    row = row + [None] * (TARGET_COLS - len(row))
                new_grid.append(row)
            else:
                new_grid.append([None] * TARGET_COLS)
        return new_grid

    def _place(
        self,
        GRID: Grid,
        TEXT: str,
        START_ROW: int,
        START_COL: int,
        ROW_DIRECTION: int,
        COL_DIRECTION: int,
    ) -> Grid:
        NEW_GRID = [ROW[:] for ROW in GRID[:]]
        for INDEX, CHAR in enumerate(TEXT):
            ROW_INDEX = START_ROW + ROW_DIRECTION * INDEX
            COL_INDEX = START_COL + COL_DIRECTION * INDEX
            NEW_GRID[ROW_INDEX][COL_INDEX] = CHAR
        return NEW_GRID

    def _place_word(self, GRID: Grid, WORD: str) -> Grid:
        current_grid = [row[:] for row in GRID[:]]

        while True:
            DIRECTIONS = self._DIRECTIONS[:]
            ROW_INDICES = list(range(len(current_grid)))
            COL_INDICES = list(
                range(len(current_grid[0]) if current_grid and current_grid[0] else 0)
            )

            shuffle(DIRECTIONS)
            shuffle(ROW_INDICES)
            shuffle(COL_INDICES)

            for DIRECTION_ROW, DIRECTION_COL in DIRECTIONS:
                for START_ROW in ROW_INDICES:
                    for START_COL in COL_INDICES:
                        COORDS = [
                            (
                                START_ROW + DIRECTION_ROW * i,
                                START_COL + DIRECTION_COL * i,
                            )
                            for i in range(len(WORD))
                        ]

                        WORD_END_INDEX = len(WORD) - 1
                        if (
                            START_ROW + DIRECTION_ROW * WORD_END_INDEX < 0
                            or START_COL + DIRECTION_COL * WORD_END_INDEX < 0
                        ):
                            continue

                        IS_COLLISION = any(
                            ROW_INDEX < len(current_grid)
                            and COL_INDEX < len(current_grid[ROW_INDEX])
                            and current_grid[ROW_INDEX][COL_INDEX] is not None
                            for ROW_INDEX, COL_INDEX in COORDS
                        )
                        if IS_COLLISION:
                            continue

                        MAX_ROW_NEEDED = max(row_index for row_index, _ in COORDS) + 1
                        MAX_COL_NEEDED = max(col_index for _, col_index in COORDS) + 1

                        EXPANDED = self._expand_grid_to(
                            current_grid, MAX_ROW_NEEDED, MAX_COL_NEEDED
                        )
                        PLACED = self._place(
                            EXPANDED,
                            WORD,
                            START_ROW,
                            START_COL,
                            DIRECTION_ROW,
                            DIRECTION_COL,
                        )
                        return PLACED

            current_grid = self._expand_grid(current_grid)

    def generate_grid(
        self, words: list[Word], number_of_words: int, FILLER: set[str]
    ) -> GridResult:
        CHOSEN_KATAKANA_WORDS = [
            word.get("katakana") for word in sample(words, number_of_words)
        ]

        grid: Grid = []
        for KATAKANA in CHOSEN_KATAKANA_WORDS:
            grid = self._place_word(grid, KATAKANA)

        FILLED_GRID = [
            [CELL if CELL is not None else choice(list(FILLER)) for CELL in ROW]
            for ROW in grid
        ]

        return GridResult(grid=FILLED_GRID, words=CHOSEN_KATAKANA_WORDS)


class WordSearchPuzzle(Mode):
    _GRID_GENERATOR = WordGrid()

    def __init__(self, words: list[Word]):
        super().__init__(words)

    def question(self) -> str:
        DEBUG = True
        UNIQUE_LETTERS = {
            LETTER for WORD in self.WORDS for LETTER in WORD.get("katakana")
        }
        FILLER_LETTERS = {"ー"} if DEBUG else UNIQUE_LETTERS
        RESULT = self._GRID_GENERATOR.generate_grid(self.WORDS, 3, FILLER_LETTERS)
        for ROW in RESULT["grid"]:
            print(*ROW, " ")

        ANSWER = RESULT.get("words")
        if DEBUG:
            print(f"Spoilers: {ANSWER}\n")
        RESPONSE = input("Which words can you spot? Enter all 3 separated by commas:\n")
        if Counter(RESPONSE.split(",")) == Counter(ANSWER):
            return "Correct!"
        else:
            return f"Wrong! The correct answers were: {ANSWER}"
