import tkinter as tk
from tkinter import messagebox, simpledialog
from game import Game
from leaderboard import Leaderboard
from difficulty import Difficulty

class UI:
    def __init__(self, game: Game, leaderboard: Leaderboard, difficulty: Difficulty):
        self.game = game
        self.leaderboard = leaderboard
        self.difficulty = difficulty
        self.root = tk.Tk()
        self.root.title('2048')
        self.grid_cells = []
        self.init_grid()
        self.update_grid()

    def init_grid(self):
        background = tk.Frame(self.root, bg='#92877d', width=400, height=400)
        background.grid(padx=(100, 100), pady=(100, 100))
        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(background, bg='#9e948a', width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text='', bg='#9e948a', justify=tk.CENTER, font=('Arial', 22, 'bold'), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.game.grid[i, j]
                if cell_value == 0:
                    self.grid_cells[i][j].configure(text='', bg='#9e948a')
                else:
                    self.grid_cells[i][j].configure(text=str(cell_value), bg=self.get_tile_color(cell_value))
        self.root.update_idletasks()

    def get_tile_color(self, value):
        colors = {
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e',
            # Add more colors for higher tiles if necessary
        }
        return colors.get(value, '#3c3a32')  # Default color for non-specified tiles

    def start(self):
        self.root.bind("<Key>", self.key_down)
        self.root.mainloop()

    def key_down(self, event):
        key = event.keysym
        if key == 'Escape':
            self.root.destroy()
        elif key in ('Up', 'Down', 'Left', 'Right'):
            direction = key.lower()
            self.game.move(direction)
            self.update_grid()
            if self.game.check_game_over():
                self.leaderboard.add_score('Player', self.game.score)
                messagebox.showinfo('Game Over', f'Your score: {self.game.score}')
                self.root.destroy()
        elif key == 'D':
            self.change_difficulty()

    def change_difficulty(self):
        new_level = simpledialog.askstring("Input", "Choose difficulty (easy, normal, hard):",
                                          parent=self.root)
        if new_level and new_level in ['easy', 'normal', 'hard']:
            self.difficulty.adjust_difficulty(new_level)
            self.difficulty.modify_gameplay(self.game)
            messagebox.showinfo('Difficulty Changed', f'New difficulty: {self.difficulty.level}')
