import pygame
from pygame import image

from game_settings import ASSETS_FOLDER_PATH, UNIT_IN_PX


class DrawHelper:
    def __init__(self, window):
        self.window = window

        paths = [
            f'{ASSETS_FOLDER_PATH}/empty.png',
            f'{ASSETS_FOLDER_PATH}/wall.png',
            f'{ASSETS_FOLDER_PATH}/food.png',
        ]
        self.images = list(map(lambda x: pygame.transform.scale(image.load(x), (UNIT_IN_PX, UNIT_IN_PX)),
                               paths
                               ))

    def draw(self, image_index, x, y):
        self.window.blit(self.images[image_index], (x, y))

    def draw_empty(self, x, y):
        self.draw(0, x, y)

    def draw_wall(self, x, y):
        self.draw(1, x, y)

    def draw_food(self, x, y):
        self.draw(2, x, y)
