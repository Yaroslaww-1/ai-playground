import time

import pygame
from pygame import display, key
import pygame.event as events

from domain.csv.game_result_csv_writer import GameResultCsvWriter
from domain.enemy.enemy import Enemy
from domain.enemy.enemy_random import EnemyRandom
from domain.enemy.enemy_search_algorighm import EnemySearchAlgorithm
from domain.game import Game
from domain.map import Map
from domain.map_filler import MapFiller
from domain.player.player_expectimax import PlayerExpectimax
from domain.player.player_minimax import PlayerMinimax
from domain.player.player_search_algorithm import PlayerSearchAlgorithm
from domain.search.search_algorithm_bfs import SearchAlgorithmBfs
from domain.search.search_algorithm_dfs import SearchAlgorithmDfs

from game.drawers.draw_helper import DrawHelper
from game.drawers.enemy_drawer import EnemyDrawer
from game.drawers.player_drawer import PlayerDrawer
from game.drawers.score_drawer import ScoreDrawer
from game.drawers.game_drawer import GameDrawer
from game_loop import GameLoop
from game.drawers.map_drawer import MapDrawer
from game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES, MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX, \
    GAME_LOOP_INTERVAL_TICK, GAME_LOOP_INTERVAL_IN_TICKS, GAME_LOOP_INTERVAL

pygame.init()
window = display.set_mode((MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX))
font = pygame.font.SysFont('Comic Sans MS', 30)

csv_writer = GameResultCsvWriter('./output.csv')


game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
map_filler = MapFiller(game_map)
map_filler.fill()


def run_game():
    start_time = time.time()

    # Map initialization
    # game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
    # map_filler = MapFiller(game_map)
    # map_filler.fill()

    # Game initialization
    game_loop = GameLoop(GAME_LOOP_INTERVAL)
    enemy_search_algorithm = SearchAlgorithmBfs(game_map)
    player = PlayerMinimax(game_map, 0, 0)
    enemies = [
        EnemySearchAlgorithm(game_map, game_map.width - 1, game_map.height - 1, enemy_search_algorithm),
        # EnemySearchAlgorithm(game_map, game_map.width - 1, game_map.height - 2, enemy_search_algorithm),
    ]
    game = Game(game_map, game_loop, player, enemies)

    # Drawers
    draw_helper = DrawHelper(window, font)
    map_drawer = MapDrawer(draw_helper)
    enemy_drawers = list(map(lambda e: EnemyDrawer(e, draw_helper), game.enemies))
    player_drawer = PlayerDrawer(game.player, draw_helper)
    score_drawer = ScoreDrawer(game.score, draw_helper)
    game_drawer = GameDrawer(map_drawer, enemy_drawers, player_drawer, score_drawer)

    game.start()
    is_game_running = True
    ticks = 0
    while is_game_running:
        pygame.time.delay(GAME_LOOP_INTERVAL_IN_TICKS * GAME_LOOP_INTERVAL_TICK)
        game.make_iteration()
        print(time.time() - start_time)
        if not game.is_game_running:
            csv_writer.write(not game.is_game_over, (time.time() - start_time) * 10, game.score.score, 'bfs')
            break

        game_drawer.draw_game(game, ticks)

        ticks += GAME_LOOP_INTERVAL_IN_TICKS

        # Handle window close
        for event in events.get():
            if event.type == pygame.QUIT:
                is_game_running = False

    game.stop()


for i in range(0, 100):
    print('game started')
    run_game()