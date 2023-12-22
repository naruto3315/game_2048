import sqlite3
from typing import List, Tuple
import logging

# Configure logging at the beginning of your script
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

class Leaderboard:
    def __init__(self, db_path: str = 'leaderboard.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT NOT NULL,
                        score INTEGER NOT NULL
                    )
                ''')
                connection.commit()
        except sqlite3.Error as e:
            logging.error(f"An error occurred while creating the table: {e.args[0]}")
            raise

    def add_score(self, player_name: str, score: int):
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO scores (player_name, score) VALUES (?, ?)
                ''', (player_name, score))
                connection.commit()
        except sqlite3.Error as e:
            logging.error(f"An error occurred while adding a score: {e.args[0]}")
            raise

    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int]]:
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?
                ''', (limit,))
                top_scores = cursor.fetchall()
                return top_scores
        except sqlite3.Error as e:
            logging.error(f"An error occurred while retrieving top scores: {e.args[0]}")
            raise
