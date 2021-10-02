import pygame
from pygame import display, key
import pygame.event as events

from domain.direction_enum import Direction
from domain.game import Game
from domain.map import Map
from domain.map_filler import MapFiller

from draw_helper import DrawHelper
from game.enemy_drawer import EnemyDrawer
from game.algorithm_drawer import AlgorithmDrawer
from game.player_drawer import PlayerDrawer
from game.score_drawer import ScoreDrawer
from game_drawer import GameDrawer
from game_loop import GameLoop
from map_drawer import MapDrawer
from game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES, MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX, \
    GAME_LOOP_INTERVAL_TICK, GAME_LOOP_INTERVAL_IN_TICKS, GAME_LOOP_INTERVAL, ENEMIES_COUNT

pygame.init()
window = display.set_mode((MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX))
font = pygame.font.SysFont('Comic Sans MS', 30)

# Map initialization
game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
map_filler = MapFiller(game_map)
map_filler.fill()
draw_helper = DrawHelper(window, font)
map_drawer = MapDrawer(draw_helper)
# Game initialization
game_loop = GameLoop(GAME_LOOP_INTERVAL)
game = Game(game_map, game_loop, ENEMIES_COUNT)

enemy_drawers = list(map(lambda e: EnemyDrawer(e, draw_helper), game.enemies))
player_drawer = PlayerDrawer(game.player, draw_helper)
score_drawer = ScoreDrawer(game.score, draw_helper)
algorithm_drawer = AlgorithmDrawer(draw_helper)

game_drawer = GameDrawer(map_drawer, enemy_drawers, player_drawer, score_drawer, algorithm_drawer)


def run_game():
    game.start()
    is_game_running = True
    ticks = 0
    pressed_keys = []
    handled_pressed_keys = set()
    ticks_from_previous_algorithm_switch = 0
    while is_game_running:
        pygame.time.delay(GAME_LOOP_INTERVAL_TICK)

        if ticks == GAME_LOOP_INTERVAL_IN_TICKS:
            ticks = 0
            game.make_iteration()

            for keys in pressed_keys:
            #     if keys[pygame.K_LEFT] and 'move' not in handled_pressed_keys:
            #         game.player.set_direction(Direction.LEFT)
            #         handled_pressed_keys.add('move')
            #     elif keys[pygame.K_RIGHT] and 'move' not in handled_pressed_keys:
            #         game.player.set_direction(Direction.RIGHT)
            #         handled_pressed_keys.add('move')
            #     elif keys[pygame.K_UP] and 'move' not in handled_pressed_keys:
            #         game.player.set_direction(Direction.UP)
            #         handled_pressed_keys.add('move')
            #     elif keys[pygame.K_DOWN] and 'move' not in handled_pressed_keys:
            #         game.player.set_direction(Direction.DOWN)
            #         handled_pressed_keys.add('move')
                if keys[pygame.K_z] and 'algorithm_switch' not in handled_pressed_keys and \
                        ticks_from_previous_algorithm_switch > 100:
                    game.switch_search_algorithm()
                    ticks_from_previous_algorithm_switch = 0
                    handled_pressed_keys.add('algorithm_switch')

            pressed_keys = []
            handled_pressed_keys.clear()

        game_drawer.draw_game(game, ticks)

        ticks += 1
        ticks_from_previous_algorithm_switch += 1

        # Handle user input
        keys = key.get_pressed()
        pressed_keys.append(keys)

        # Handle window close
        for event in events.get():
            if event.type == pygame.QUIT:
                is_game_running = False


    game.stop()


run_game()