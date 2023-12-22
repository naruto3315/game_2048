## difficulty.py

class Difficulty:
    def __init__(self, level='normal'):
        self.level = level
        self.probability_new_tile_4 = self._get_probability_new_tile_4()

    def _get_probability_new_tile_4(self):
        probabilities = {
            'easy': 0.05,
            'normal': 0.1,
            'hard': 0.2
        }
        return probabilities.get(self.level, 0.1)  # default to 'normal' probability

    def adjust_difficulty(self, level: str):
        valid_levels = ['easy', 'normal', 'hard']
        if level not in valid_levels:
            raise ValueError(f"Invalid difficulty level: {level}. Valid options are: {valid_levels}")
        self.level = level
        self.probability_new_tile_4 = self._get_probability_new_tile_4()

    def modify_gameplay(self, game):
        if hasattr(game, 'set_probability_new_tile_4'):
            game.set_probability_new_tile_4(self.probability_new_tile_4)
        else:
            raise AttributeError("Game class does not have a method set_probability_new_tile_4")
