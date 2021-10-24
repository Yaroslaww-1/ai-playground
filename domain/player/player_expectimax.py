from typing import List

from domain.direction_enum import Direction
from domain.minimax.expectimax import Expectimax
from domain.minimax.minimax import Minimax
from domain.player.player import Player
from domain.position import Position
from domain.score import Score
from domain.search.search_algorithm import SearchAlgorithm


class PlayerExpectimax(Player):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)

    def get_next_direction(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> Direction:
        next_position = Expectimax().find_optimal_next_position(
            self.map,
            Position(self.x, self.y),
            enemy_positions,
            score
        )
        return self.map.get_direction_from_to_positions(self.x, self.y, next_position.x, next_position.y)

    def move_to_next_position(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> None:
        next_position = self.get_next_position()
        self.set_position(next_position)
        self.direction = self.get_next_direction(enemy_positions, score)
