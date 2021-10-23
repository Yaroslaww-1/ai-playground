from domain.direction_enum import Direction
from domain.player.player import Player
from game.game_settings import UNIT_IN_PX, MOVE_PX_PER_TICK


class CharacterDrawer:
    def __init__(self, character, drawer_helper):
        self.character = character
        self.x = character.x * UNIT_IN_PX
        self.y = character.y * UNIT_IN_PX
        self.drawer_helper = drawer_helper

    def draw_character(self, ticks):
        movement_in_px = ticks * MOVE_PX_PER_TICK

        x = self.character.x * UNIT_IN_PX
        y = self.character.y * UNIT_IN_PX

        # if self.character.can_move_in_direction() and self.character.is_moving:
        #     if self.character.direction == Direction.UP:
        #         y -= movement_in_px
        #     if self.character.direction == Direction.DOWN:
        #         y += movement_in_px
        #     if self.character.direction == Direction.LEFT:
        #         x -= movement_in_px
        #     if self.character.direction == Direction.RIGHT:
        #         x += movement_in_px

        if isinstance(self.character, Player):
            self.drawer_helper.draw_player(x, y)
        else:
            self.drawer_helper.draw_enemy(x, y)
