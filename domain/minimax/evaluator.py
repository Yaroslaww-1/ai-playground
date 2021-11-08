import math
import random
from typing import List

from domain.position import Position
from domain.search.search_algorithm_bfs import SearchAlgorithmBfs


class Evaluator:
    def __init__(self, map):
        self.map = map

    def evaluate(self, position: Position, enemy_positions: List[Position], has_point: bool, points_left: List[Position]):
        min_distance_to_enemy = math.inf
        search_algorithm = SearchAlgorithmBfs(self.map)
        for enemy_position in enemy_positions:
            distance_to_enemy = len(search_algorithm.find_path(position, enemy_position))
            min_distance_to_enemy = min(min_distance_to_enemy, distance_to_enemy)

        min_distance_to_point = math.inf
        for point_position in points_left:
            distance_to_point = abs(point_position.x - position.x) + abs(point_position.y - position.y)
            min_distance_to_point = min(min_distance_to_point, distance_to_point)

        # for minimax TODO: move to separate evaluator
        # print(has_point,  math.log(min_distance_to_enemy + 1, 1.25) + has_point * 10000)
        # return math.log(min_distance_to_enemy + 1, 1.25) + has_point * 5

        # for expectimax
        value = math.log(min_distance_to_enemy + 1, 1.25) +\
                has_point * (50 - len(points_left)) / 20 +\
                math.log(min_distance_to_point + 1, 1.25) * (50 - len(points_left)) / 30 * random.randrange(100, 200) / 100
        print(f"value {value} for {position}, {has_point}, {min_distance_to_enemy}")
        return value
