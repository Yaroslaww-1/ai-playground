import random
from enum import IntEnum

from pacman.domain.position import Position


class MapTileInner(IntEnum):
    EMPTY = 0
    WALL = 1
    EMPTY_BUT_LOCKED = 2


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class MapFiller:
    def __init__(self, map):
        self.width = map.width
        self.height = map.height
        self.map = map

    def fill(self):
        self.lock_borderline_tiles()
        for x in range(self.width):
            for y in range(self.height):
                if self.map.is_tile_equals(x, y, MapTileInner.EMPTY):
                    self.generate_wall(x, y)
        self.prepare_map_for_return()

    def lock_borderline_tiles(self):
        for x in range(self.width):
            self.map.set_tile(x, 0, MapTileInner.EMPTY_BUT_LOCKED)
            self.map.set_tile(x, self.height - 1, MapTileInner.EMPTY_BUT_LOCKED)
        for y in range(self.height):
            self.map.set_tile(0, y, MapTileInner.EMPTY_BUT_LOCKED)
            self.map.set_tile(self.width - 1, y, MapTileInner.EMPTY_BUT_LOCKED)

    def generate_wall(self, x, y):
        MAX_WALL_LENGTH = 10
        wall_length = random.randint(0, MAX_WALL_LENGTH)
        wall_tiles = []
        current_x = x
        current_y = y
        for i in range(wall_length):
            self.map.set_tile(current_x, current_y, MapTileInner.WALL)
            position = self.get_random_adjacent_position(current_x, current_y)
            if position is None:
                break
            current_x = position.x
            current_y = position.y
            wall_tiles.append(position)
        self.lock_adjacent_to_wall_positions(wall_tiles)

    def get_random_adjacent_position(self, x, y):
        directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        random.shuffle(directions)
        for direction in directions:
            # UP and DOWN
            if direction == Direction.UP and y > 0 and self.map.is_tile_equals(x, y - 1, MapTileInner.EMPTY):
                return Position(x, y - 1)
            if direction == Direction.DOWN and y < self.height - 1 and self.map.is_tile_equals(x, y + 1, MapTileInner.EMPTY):
                return Position(x, y + 1)
            # LEFT and RIGHT
            if direction == Direction.RIGHT and x < self.width - 1 and self.map.is_tile_equals(x + 1, y, MapTileInner.EMPTY):
                return Position(x + 1, y)
            if direction == Direction.LEFT and x > 0 and self.map.is_tile_equals(x - 1, y, MapTileInner.EMPTY):
                return Position(x - 1, y)
        return None

    def lock_adjacent_to_wall_positions(self, wall_tiles):
        for tile in wall_tiles:
            self.lock_all_empty_adjacent_positions(tile.x, tile.y)

    def lock_all_empty_adjacent_positions(self, x, y):
        start_x = x - 1 if x > 0 else x
        end_x = x + 1 if x < self.width - 1 else x
        start_y = y - 1 if y > 0 else y
        end_y = y + 1 if y < self.height - 1 else y
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if self.map.is_tile_equals(x, y, MapTileInner.EMPTY):
                    self.map.set_tile(x, y, MapTileInner.EMPTY_BUT_LOCKED)

    def prepare_map_for_return(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.map.is_tile_equals(x, y, MapTileInner.EMPTY_BUT_LOCKED):
                    self.map.set_tile(x, y, MapTileInner.EMPTY)
