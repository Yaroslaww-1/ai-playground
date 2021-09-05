from enum import IntEnum
import random

from pacman.domain.position import Position


class MapTile(IntEnum):
    EMPTY = 0
    WALL = 1


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[MapTile.EMPTY for x in range(self.width)] for y in range(self.height)]

    def set_tiles(self, tiles):
        self.tiles = tiles

    def set_tile(self, x, y, value):
        self.tiles[y][x] = value

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def is_tile_equals(self, x, y, value_to_compare):
        return self.get_tile(x, y) == value_to_compare

    def get_random_adjacent_position(self, x, y):
        directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        random.shuffle(directions)
        for direction in directions:
            # UP and DOWN
            if direction == Direction.UP and y > 0 and self.is_tile_equals(x, y - 1, MapTile.EMPTY):
                return Position(x, y - 1)
            if direction == Direction.DOWN and y < self.height - 1 and self.is_tile_equals(x, y + 1, MapTile.EMPTY):
                return Position(x, y + 1)
            # LEFT and RIGHT
            if direction == Direction.RIGHT and x < self.width - 1 and self.is_tile_equals(x + 1, y, MapTile.EMPTY):
                return Position(x + 1, y)
            if direction == Direction.LEFT and x > 0 and self.is_tile_equals(x - 1, y, MapTile.EMPTY):
                return Position(x - 1, y)
        return None