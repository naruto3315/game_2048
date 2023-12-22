## main.py

import tkinter as tk
from game import Game
from leaderboard import Leaderboard
from difficulty import Difficulty
from ui import UI

def main():
    # Initialize the game, leaderboard, difficulty, and UI classes
    game = Game()
    leaderboard = Leaderboard()
    difficulty = Difficulty()
    ui = UI(game, leaderboard, difficulty)

    # Start the game UI
    ui.start()

    # After the game is over, display the top scores
    top_scores = leaderboard.get_top_scores()
    print("Top Scores:")
    for name, score in top_scores:
        print(f"{name}: {score}")

if __name__ == "__main__":
    main()
