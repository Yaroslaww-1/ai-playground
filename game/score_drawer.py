from pygame import display

from domain.direction_enum import Direction
from domain.player import Player
from game.game_settings import UNIT_IN_PX, MOVE_PX_PER_TICK, GAME_LOOP_INTERVAL_IN_TICKS


class ScoreDrawer:
    def __init__(self, score, drawer_helper):
        self.score = score
        self.drawer_helper = drawer_helper

    def draw_score(self):
        self.drawer_helper.draw_text(0, 0, f'Score: {self.score.score}')
