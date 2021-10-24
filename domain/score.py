import numpy

from domain.map import MapTile
from domain.position import Position


class Score:
    def __init__(self, map):
        self.map = map
        self.available_points = self.get_initial_available_points()
        self.score = 0

    def get_initial_available_points(self):
        available_point_coordinates = []
        for x in range(self.map.width):
            for y in range(self.map.height):
                if self.map.is_tile_equals(x, y, MapTile.EMPTY):
                    available_point_coordinates.append(Position(x, y))
        return available_point_coordinates

    def handle_player_move(self, player_x, player_y):
        for available_point in self.available_points:
            if available_point.x == player_x and available_point.y == player_y:
                self.remove_available_point(available_point)
                self.score += 1

    def set_available_points(self, available_points=[]):
        should_notify = True if numpy.array_equal(self.available_points, available_points) else False
        self.available_points = available_points

    def remove_available_point(self, point_position):
        self.available_points.remove(point_position)

    def reset(self):
        self.available_points = self.get_initial_available_points()
        self.score = 0

    def has_point(self, position: Position):
        for available_point in self.available_points:
            if available_point.x == position.x and available_point.y == position.y:
                return True
        return False
