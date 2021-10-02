import random

from domain.direction_enum import Direction
from domain.direction_helper import DirectionHelper
from domain.position import Position


class Character:
    def __init__(self, map, initial_x, initial_y):
        self.map = map
        self.x = initial_x
        self.y = initial_y
        self.is_moving = False
        self.direction = DirectionHelper.get_random_directions()[0]

    def get_position(self):
        return Position(self.x, self.y)

    def set_position(self, position):
        self.x = position.x
        self.y = position.y

    def set_direction(self, direction):
        if self.is_moving:
            pass
        self.direction = direction

    def can_move_in_direction(self):
        if self.map.get_next_position_in_direction(self.x, self.y, self.direction) is not None:
            return True
        else:
            return False

    def move_left(self):
        if self.map.is_position_exist(self.x - 1, self.y):
            self.is_moving = True
            self.set_position(Position(self.x - 1, self.y))
        else:
            self.is_moving = False

    def move_right(self):
        if self.map.is_position_exist(self.x + 1, self.y):
            self.is_moving = True
            self.set_position(Position(self.x + 1, self.y))
        else:
            self.is_moving = False

    def move_up(self):
        if self.map.is_position_exist(self.x, self.y - 1):
            self.is_moving = True
            self.set_position(Position(self.x, self.y - 1))
        else:
            self.is_moving = False

    def move_down(self):
        if self.map.is_position_exist(self.x, self.y + 1):
            self.is_moving = True
            self.set_position(Position(self.x, self.y + 1))
        else:
            self.is_moving = False
