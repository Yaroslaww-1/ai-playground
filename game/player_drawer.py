from pygame import display

from domain.direction_enum import Direction
from game.character_drawer import CharacterDrawer
from game.game_settings import UNIT_IN_PX


class PlayerDrawer(CharacterDrawer):
    def __init__(self, player, drawer_helper):
        super().__init__(player, drawer_helper)
        self.player = player
        self.drawer_helper = drawer_helper

    def draw_player(self, ticks):
        self.draw_character(ticks)
