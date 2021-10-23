import math
from typing import List

from domain.position import Position
from domain.search.search_algorithm_bfs import SearchAlgorithmBfs


class Evaluator:
    def __init__(self, map):
        self.map = map

    def evaluate(self, position: Position, enemy_positions: List[Position], has_point: bool):
        min_distance_to_enemy = math.inf
        search_algorithm = SearchAlgorithmBfs(self.map)
        for enemy_position in enemy_positions:
            distance_to_enemy = len(search_algorithm.find_path(position, enemy_position))
            min_distance_to_enemy = min(min_distance_to_enemy, distance_to_enemy)

        return min_distance_to_enemy * 0.1 + has_point
