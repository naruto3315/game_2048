## game.py

import numpy as np

class Game:
    def __init__(self, size=4):
        self.grid = np.zeros((size, size), dtype=int)
        self.score = 0
        self.state = 'playing'
        self.add_new_tile()
        self.add_new_tile()
    
    def move(self, direction: str):
        if direction not in ['up', 'down', 'left', 'right']:
            raise ValueError("Invalid move direction")

        if self.state != 'playing':
            return

        original_grid = self.grid.copy()
        if direction in ['up', 'down']:
            self.grid = self._move_vertical(direction == 'down')
        else:
            self.grid = self._move_horizontal(direction == 'right')

        if not np.array_equal(original_grid, self.grid):
            self.add_new_tile()

    def _move_vertical(self, reverse=False):
        for col in range(self.grid.shape[1]):
            column = self.grid[:, col] if not reverse else self.grid[::-1, col]
            merged = self._merge_tiles(column)
            new_column = np.zeros_like(column)
            new_column[:len(merged)] = merged
            if reverse:
                new_column = new_column[::-1]
            self.grid[:, col] = new_column
        return self.grid

    def _move_horizontal(self, reverse=False):
        for row in range(self.grid.shape[0]):
            line = self.grid[row, :] if not reverse else self.grid[row, ::-1]
            merged = self._merge_tiles(line)
            new_line = np.zeros_like(line)
            new_line[:len(merged)] = merged
            if reverse:
                new_line = new_line[::-1]
            self.grid[row, :] = new_line
        return self.grid

    def _merge_tiles(self, tiles):
        non_zero = tiles[tiles != 0]
        merged = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                self.score += merged_value
                merged.append(merged_value)
                skip = True
            else:
                merged.append(non_zero[i])
        return np.array(merged)

    def check_game_over(self) -> bool:
        if np.any(self.grid == 0):
            return False
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if j + 1 < self.grid.shape[1] and self.grid[i, j] == self.grid[i, j + 1]:
                    return False
                if i + 1 < self.grid.shape[0] and self.grid[i, j] == self.grid[i + 1, j]:
                    return False
        self.state = 'game_over'
        return True

    def add_new_tile(self):
        empty_cells = np.argwhere(self.grid == 0)
        if empty_cells.size > 0:
            y, x = empty_cells[np.random.choice(empty_cells.shape[0])]
            self.grid[y, x] = np.random.choice([2, 4], p=[0.9, 0.1])
