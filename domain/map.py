from enum import IntEnum

from domain.direction_enum import Direction
from domain.direction_helper import DirectionHelper
from domain.position import Position


class MapTile(IntEnum):
    EMPTY = 0
    WALL = 1


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

    def get_random_opened_direction(self, x, y):
        directions = DirectionHelper.get_random_directions()
        for direction in directions:
            if self.get_next_position_in_direction(x, y, direction) is not None:
                return direction
        return None

    def get_all_opened_directions(self, x, y):
        opened_directions = []
        directions = DirectionHelper.get_random_directions()
        for direction in directions:
            if self.get_next_position_in_direction(x, y, direction) is not None:
                opened_directions.append(direction)
        return opened_directions

    def get_next_position_in_direction(self, x, y, direction):
        if direction == Direction.UP and self.is_position_exist(x, y - 1) and self.is_tile_equals(x, y - 1, MapTile.EMPTY):
            return Position(x, y - 1)
        if direction == Direction.DOWN and self.is_position_exist(x, y + 1) and self.is_tile_equals(x, y + 1, MapTile.EMPTY):
            return Position(x, y + 1)
        if direction == Direction.RIGHT and self.is_position_exist(x + 1, y) and self.is_tile_equals(x + 1, y, MapTile.EMPTY):
            return Position(x + 1, y)
        if direction == Direction.LEFT and self.is_position_exist(x - 1, y) and self.is_tile_equals(x - 1, y, MapTile.EMPTY):
            return Position(x - 1, y)
        return None

    def get_random_adjacent_position(self, x, y):
        direction = self.get_random_opened_direction(x, y)
        return self.get_next_position_in_direction(x, y, direction)

    def is_position_exist(self, x, y):
        if 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1:
            return True
        else:
            return False