from copy import deepcopy
from typing import List

from domain.position import Position


class Score:
    def __init__(self, available_points: List[Position], initial_score=0):
        self.map = map
        self.available_points = deepcopy(available_points)
        self.score = initial_score

    def handle_player_move(self, player_x, player_y):
        for available_point in self.available_points:
            if available_point.x == player_x and available_point.y == player_y:
                self.remove_available_point(available_point)
                self.score += 50

    def remove_available_point(self, point_position):
        if self.available_points.count(point_position) > 0:
            self.available_points.remove(point_position)

    def add_available_point(self, point_position):
        self.available_points.append(point_position)

    def has_point(self, position: Position):
        for available_point in self.available_points:
            if available_point.x == position.x and available_point.y == position.y:
                return True
        return False
