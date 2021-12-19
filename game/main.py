import time

import pygame
from pygame import display, key
import pygame.event as events

from domain.csv.game_result_csv_writer import GameResultCsvWriter
from domain.enemy.enemy import Enemy
from domain.enemy.enemy_random import EnemyRandom
from domain.enemy.enemy_search_algorighm import EnemySearchAlgorithm
from domain.game import Game
from domain.game_state import GameState
from domain.map import Map
from domain.player.player_dqn import PlayerDQN
from domain.position import Position
from domain.score import Score
from domain.search.search_algorithm_bfs import SearchAlgorithmBfs

from game.drawers.draw_helper import DrawHelper
from game.drawers.enemy_drawer import EnemyDrawer
from game.drawers.player_drawer import PlayerDrawer
from game.drawers.score_drawer import ScoreDrawer
from game.drawers.game_drawer import GameDrawer
from game.map_tiles_example import map_tiles_example, available_points_example
from game.drawers.map_drawer import MapDrawer
from game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES, MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX, \
    GAME_LOOP_INTERVAL_TICK, GAME_LOOP_INTERVAL_IN_TICKS

WITH_UI = True

if WITH_UI:
    pygame.init()
    window = display.set_mode((MAP_WIDTH_IN_PX, MAP_HEIGHT_IN_PX))
    font = pygame.font.SysFont('Comic Sans MS', 30)

csv_writer = GameResultCsvWriter('./output.csv')


def run_games():
    # Map initialization
    game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
    game_map.set_tiles(map_tiles_example)

    player = PlayerDQN(game_map, 0, 0)

    for i in range(10000):
        # Map initialization
        game_map = Map(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
        game_map.set_tiles(map_tiles_example)

        # Game initialization
        enemy_search_algorithm = SearchAlgorithmBfs(game_map)

        enemies = [
            EnemySearchAlgorithm(game_map, game_map.width - 1, game_map.height - 1, enemy_search_algorithm),
            # EnemySearchAlgorithm(game_map, game_map.width - 1, game_map.height - 2, enemy_search_algorithm),
        ]
        score = Score(available_points_example)
        game = Game(game_map, score, player, enemies)

        if WITH_UI:
            # Drawers initialization
            draw_helper = DrawHelper(window, font)
            map_drawer = MapDrawer(draw_helper)
            enemy_drawers = list(map(lambda e: EnemyDrawer(e, draw_helper), game.enemies))
            player_drawer = PlayerDrawer(game.player, draw_helper)
            score_drawer = ScoreDrawer(game.score, draw_helper)
            game_drawer = GameDrawer(map_drawer, enemy_drawers, player_drawer, score_drawer)

        game.start()
        ticks = 0
        while True:
            if WITH_UI:
                pygame.time.delay(GAME_LOOP_INTERVAL_IN_TICKS * GAME_LOOP_INTERVAL_TICK)
            game.make_iteration()

            if WITH_UI:
                game_drawer.draw_game(game, ticks)

            # ticks += GAME_LOOP_INTERVAL_IN_TICKS

            if not game.is_game_running:
                break

            # # Handle window close
            # for event in events.get():
            #     if event.type == pygame.QUIT:
            #         is_game_running = False

        final_game_state = GameState(
            game_map,
            game.score,
            Position(game.player.x, game.player.y),
            game.player.direction,
            [Position(e.x, e.y) for e in game.enemies]
        )
        player.finalize(final_game_state)
        player.reset(Score(available_points_example), [Position(game_map.width - 1, game_map.height - 1)])


run_games()