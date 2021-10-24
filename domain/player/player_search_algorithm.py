import random
from typing import List

from domain.direction_enum import Direction
from domain.player.player import Player
from domain.position import Position
from domain.score import Score
from domain.search.search_algorithm import SearchAlgorithm


class PlayerSearchAlgorithm(Player):
    def __init__(self, map, initial_x, initial_y, search_algorithm: SearchAlgorithm):
        super().__init__(map, initial_x, initial_y)
        self.search_algorithm = search_algorithm

    def get_next_direction(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> Direction:
        random_point_position = random.choice(score.available_points)
        optimal_path = self.search_algorithm.find_path(
            Position(self.x, self.y),
            Position(random_point_position.x, random_point_position.y)
        )
        for next_position in optimal_path:
            if next_position.x != self.x or next_position.y != self.y:
                return self.map.get_direction_from_to_positions(self.x, self.y, next_position.x, next_position.y)
        return self.map.get_direction_from_to_positions(self.x, self.y, optimal_path[0].x, optimal_path[0].y)

    def move_to_next_position(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> None:
        next_position = self.get_next_position()
        self.set_position(next_position)
        self.direction = self.get_next_direction(enemy_positions, score)
