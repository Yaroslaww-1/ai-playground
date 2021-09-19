import pygame
from pygame import display, key
import pygame.event as events


from domain.game import Game
from domain.map import Map
from domain.map_filler import MapFiller

from draw_helper import DrawHelper
from game_drawer import GameDrawer
from game_loop import GameLoop
from map_drawer import MapDrawer
from game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES, MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX, GAME_LOOP_INTERVAL

pygame.init()
window = display.set_mode((MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX))

# Map initialization
map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
map_filler = MapFiller(map)
map_filler.fill()
draw_helper = DrawHelper(window)
map_drawer = MapDrawer(draw_helper)
# Game initialization
game_loop = GameLoop(GAME_LOOP_INTERVAL)
game = Game(map, game_loop)
game_drawer = GameDrawer(map_drawer)


def run_game():
    game.start()
    is_game_running = True
    while is_game_running:
        pygame.time.delay(GAME_LOOP_INTERVAL)
        game_drawer.draw_game(game)
        for event in events.get():
            if event.type == pygame.QUIT:
                is_game_running = False
    game.stop()


run_game()