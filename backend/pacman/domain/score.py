import numpy

from pacman.domain.map import MapTile
from pacman.domain.position import Position


class Score:
    def __init__(self, map, score_changed_listener):
        self.map = map
        self.available_points = self.get_initial_available_points()
        self.score = 0
        self.score_changed_listener = score_changed_listener

    def get_initial_available_points(self):
        available_point_coordinates = []
        for x in range(self.map.width):
            for y in range(self.map.height):
                if self.map.is_tile_equals(x, y, MapTile.EMPTY):
                    available_point_coordinates.append(Position(x, y))
        return available_point_coordinates

    def handle_player_move(self, player_position):
        for available_point in self.available_points:
            if available_point.x == player_position.x and available_point.y == player_position.y:
                self.remove_available_point(available_point)
                self.score += 1

    def set_available_points(self, available_points=[]):
        should_notify = True if numpy.array_equal(self.available_points, available_points) else False
        self.available_points = available_points
        if should_notify:
            self.score_changed_listener(self)

    def remove_available_point(self, point_position):
        self.available_points.remove(point_position)
        self.score_changed_listener(self)