import pygame
import pygame.event as events

class GameDrawer:
    def __init__(self, map_drawer):
        self.map_drawer = map_drawer

    def draw_game(self, game):
        self.map_drawer.draw_map(game.map)
