from copy import deepcopy
from random import sample, shuffle, choice
from typing import TypedDict
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
        WIDTH = max((len(row) for row in grid), default=1)
        new_rows = [row[:] + [None] for row in grid]
        new_rows.append([None] * (WIDTH + 1))
        return new_rows

    def _expand_grid_to(self, GRID: Grid, MINIMUM_ROWS: int, MINIMUM_COLS: int) -> Grid:
        HEIGHT = len(GRID)
        WIDTH = len(GRID[0]) if GRID and GRID[0] else 0
        TARGET_ROWS = max(HEIGHT, MINIMUM_ROWS)
        TARGET_COLS = max(WIDTH, MINIMUM_COLS)

        NEW_GRID: Grid = [[None] * TARGET_COLS for _ in range(TARGET_ROWS)]

        for ROW_INDEX, ROW in enumerate(GRID):
            for COL_INDEX, _ in enumerate(ROW):
                CELL = GRID[ROW_INDEX][COL_INDEX]
                if CELL:
                    NEW_GRID[ROW_INDEX][COL_INDEX] = CELL

        return NEW_GRID

    def _place(
        self,
        GRID: Grid,
        TEXT: str,
        START_ROW: int,
        START_COL: int,
        ROW_DIRECTION: int,
        COL_DIRECTION: int,
    ) -> Grid:
        NEW_GRID = deepcopy(GRID)
        for INDEX, CHAR in enumerate(TEXT):
            ROW_INDEX = START_ROW + ROW_DIRECTION * INDEX
            COL_INDEX = START_COL + COL_DIRECTION * INDEX
            NEW_GRID[ROW_INDEX][COL_INDEX] = CHAR
        return NEW_GRID

    def _place_word(self, GRID: Grid, WORD: str) -> Grid:
        current_grid = deepcopy(GRID)

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
                                START_ROW + DIRECTION_ROW * INDEX,
                                START_COL + DIRECTION_COL * INDEX,
                            )
                            for INDEX in range(len(WORD))
                        ]

                        WORD_END_INDEX = len(WORD) - 1
                        WORD_END_ROW = START_ROW + DIRECTION_ROW * WORD_END_INDEX
                        WORD_END_COL = START_COL + DIRECTION_COL * WORD_END_INDEX
                        IS_OUT_OF_BOUNDS = WORD_END_ROW < 0 or WORD_END_COL < 0
                        if IS_OUT_OF_BOUNDS:
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

                        return self._place(
                            EXPANDED,
                            WORD,
                            START_ROW,
                            START_COL,
                            DIRECTION_ROW,
                            DIRECTION_COL,
                        )

            current_grid = self._expand_grid(current_grid)

    def generate_grid(
        self, words: list[Word], number_of_words: int, FILLER: frozenset[str]
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
