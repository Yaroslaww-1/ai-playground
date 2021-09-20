from pygame import display

from domain.direction_enum import Direction
from domain.player import Player
from game.game_settings import UNIT_IN_PX, MOVE_PX_PER_TICK, GAME_LOOP_INTERVAL_IN_TICKS


class ScoreDrawer:
    def __init__(self, score, drawer_helper):
        self.score = score
        self.drawer_helper = drawer_helper

    def draw_score(self, game):
        self.drawer_helper.draw_text(0, 0, f'Score: {self.score.score}')
        for available_point in self.score.available_points:
            is_tile_without_character_or_wall = game.is_tile_without_character_or_wall(available_point.x, available_point.y)
            # is_character_not_moving_in_tile = True

            # for enemy in game.enemies:
            #     if enemy.get_next_position() is not None and enemy.get_next_position().x == available_point.x and enemy.get_next_position().y == available_point.y:
            #         is_enemy_not_moving_in_tile = False
            if is_tile_without_character_or_wall:
                self.drawer_helper.draw_food(available_point.x * UNIT_IN_PX, available_point.y * UNIT_IN_PX)

    def draw_game_over(self, game):
        self.drawer_helper.draw_text(0, 0, f'Game over')