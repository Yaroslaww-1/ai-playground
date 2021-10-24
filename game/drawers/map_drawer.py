from pygame import display

from domain.map import MapTile
from game_settings import UNIT_IN_PX


class MapDrawer:
    def __init__(self, draw_helper):
        self.draw_helper = draw_helper

    def draw_map(self, map):
        for y in range(map.height):
            for x in range(map.width):
                tile = map.get_tile(x, y)
                self.draw_tile(tile, x * UNIT_IN_PX, y * UNIT_IN_PX)

    def draw_tile(self, tile, x, y):
        if tile == MapTile.EMPTY:
            self.draw_helper.draw_empty(x, y)
        if tile == MapTile.WALL:
            self.draw_helper.draw_wall(x, y)
