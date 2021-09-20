import pygame
from pygame import display, key
import pygame.event as events

from domain.direction_enum import Direction
from domain.game import Game
from domain.map import Map
from domain.map_filler import MapFiller

from draw_helper import DrawHelper
from game.enemy_drawer import EnemyDrawer
from game.player_drawer import PlayerDrawer
from game_drawer import GameDrawer
from game_loop import GameLoop
from map_drawer import MapDrawer
from game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES, MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX, \
    GAME_LOOP_INTERVAL_TICK, GAME_LOOP_INTERVAL_IN_TICKS, GAME_LOOP_INTERVAL

pygame.init()
window = display.set_mode((MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX))

# Map initialization
game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
map_filler = MapFiller(game_map)
map_filler.fill()
draw_helper = DrawHelper(window)
map_drawer = MapDrawer(draw_helper)
# Game initialization
game_loop = GameLoop(GAME_LOOP_INTERVAL)
game = Game(game_map, game_loop)

enemy_drawers = list(map(lambda e: EnemyDrawer(e, draw_helper), game.enemies))
player_drawer = PlayerDrawer(game.player, draw_helper)

game_drawer = GameDrawer(map_drawer, enemy_drawers, player_drawer)


def run_game():
    game.start()
    is_game_running = True
    ticks = 0
    while is_game_running:
        pygame.time.delay(GAME_LOOP_INTERVAL_TICK)

        if ticks == GAME_LOOP_INTERVAL_IN_TICKS:
            ticks = 0
            game.make_iteration()

            # Handle user input
            keys = key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.player.set_direction(Direction.LEFT)
            elif keys[pygame.K_RIGHT]:
                game.player.set_direction(Direction.RIGHT)
            elif keys[pygame.K_UP]:
                game.player.set_direction(Direction.UP)
            elif keys[pygame.K_DOWN]:
                game.player.set_direction(Direction.DOWN)

        game_drawer.draw_game(game, ticks)

        ticks += 1

        # Handle window close
        for event in events.get():
            if event.type == pygame.QUIT:
                is_game_running = False


    game.stop()


run_game()