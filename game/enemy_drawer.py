from pygame import display

from game.character_drawer import CharacterDrawer


class EnemyDrawer(CharacterDrawer):
    def __init__(self, enemy, drawer_helper):
        super().__init__(enemy, drawer_helper)
        self.enemy = enemy
        self.drawer_helper = drawer_helper

    def draw_enemy(self, ticks):
        self.draw_character(ticks)
