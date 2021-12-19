from typing import List

from domain.direction_enum import Direction
from domain.map import Map
from domain.position import Position
from domain.score import Score


class GameState:
    def __init__(
            self,
            map: Map,
            score: Score,
            player_position: Position,
            player_direction: Direction,
            enemy_positions: List[Position]):
        self.map = map
        self.score = score
        self.player_position = player_position
        self.player_direction = player_direction
        self.enemy_positions = enemy_positions

    # def can_player_move_in_current_direction(self):
    #     return self.map.get_next_position_in_direction(
    #         self.player_position.x,
    #         self.player_position.y,
    #         self.player_direction
    #     ) is not None
