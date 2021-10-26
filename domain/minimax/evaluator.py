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

        # for minimax TODO: move to separate evaluator
        # print(has_point,  math.log(min_distance_to_enemy + 1, 1.25) + has_point * 10000)
        # return math.log(min_distance_to_enemy + 1, 1.25) + has_point * 5

        # for expectimax
        return math.log(min_distance_to_enemy + 1, 1.25) + has_point
