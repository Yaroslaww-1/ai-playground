import random

from domain.character import Character
from domain.direction_enum import Direction
from domain.direction_helper import DirectionHelper
from domain.position import Position


class Player(Character):
    def __init__(self, map, initial_x, initial_y, on_move):
        super().__init__(map, initial_x, initial_y)
        self.map = map
        self.on_move = on_move
        self.is_moving = True
        self.direction = Direction.RIGHT

    def set_position(self, position):
        self.x = position.x
        self.y = position.y
        self.on_move()
