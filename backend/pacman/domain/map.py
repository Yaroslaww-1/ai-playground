from enum import IntEnum


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
