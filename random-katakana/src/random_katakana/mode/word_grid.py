import random


class WordGrid:
    _DIRECTIONS = [
        (0, 1),  # →
        (0, -1),  # ←
        (1, 0),  # ↓
        (-1, 0),  # ↑
        (1, 1),  # ↘
        (1, -1),  # ↙
        (-1, 1),  # ↗
        (-1, -1),  # ↖
    ]

    def _expand_grid(self, grid):
        width = max(len(row) for row in grid) if grid else 1
        grid.append([None] * width)
        for row in grid:
            row.append(None)

    def _expand_grid_to(self, grid, min_rows, min_cols):
        while len(grid) < min_rows:
            grid.append([None] * (len(grid[0]) if grid else 0))
        for i in range(len(grid)):
            while len(grid[i]) < min_cols:
                grid[i].append(None)

    def _can_place(self, grid, word, r, c, dr, dc):
        coords = [(r + dr * i, c + dc * i) for i in range(len(word))]
        if any(rr < 0 or cc < 0 for rr, cc in coords):
            return False
        max_r = max(rr for rr, _ in coords) + 1
        max_c = max(cc for _, cc in coords) + 1
        self._expand_grid_to(grid, max_r, max_c)
        for (rr, cc), ch in zip(coords, word):
            if grid[rr][cc] is not None:
                return False
        return True

    def _place(self, grid, word, r, c, dr, dc):
        for i, ch in enumerate(word):
            rr = r + dr * i
            cc = c + dc * i
            grid[rr][cc] = ch

    def _place_word(self, grid, word):
        while True:
            directions = self._DIRECTIONS[:]
            random.shuffle(directions)  # shuffle directions
            rows = list(range(len(grid)))
            cols = list(range(len(grid[0])) if grid else [0])
            random.shuffle(rows)
            random.shuffle(cols)

            for dr, dc in directions:
                for r in rows:
                    for c in cols:
                        if self._can_place(grid, word, r, c, dr, dc):
                            self._place(grid, word, r, c, dr, dc)
                            return
            # If no placement found → expand grid
            self._expand_grid(grid)

    def generate_grid(self, words):
        grid = [[None]]
        for word in words:
            self._place_word(grid, word)

        return [[cell if cell is not None else " " for cell in row] for row in grid]
