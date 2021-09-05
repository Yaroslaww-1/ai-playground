import asyncio

from pacman.domain.enemy_behavior_random import EnemyBehaviourRandom
from pacman.domain.position import Position
from pacman.domain.lib.thread_job import ThreadJob


class Game:
    def __init__(self, map, enemy_behaviour, enemy_count=3):
        self.map = map
        self.enemy_count = enemy_count
        self.player_position = self.get_initial_player_position()
        self.enemy_positions = self.get_initial_enemies_position()
        self.game_loop = None
        self.enemy_behaviour = enemy_behaviour
        self.enemy_positions_changed_listener = lambda x: x
        self.game_over_lister = lambda x: x

    def get_initial_player_position(self):
        return Position(0, 0)

    def get_initial_enemies_position(self):
        enemy_positions = []
        for i in range(self.enemy_count):
            # always locate enemies at the last column
            x = self.map.width - 1
            y = self.map.height - 1 - i
            enemy_positions.append(Position(x, y))
        return enemy_positions

    def start(self, enemy_positions_changed_listener, game_over_lister):
        self.enemy_positions_changed_listener = enemy_positions_changed_listener
        self.game_over_lister = game_over_lister
        self.game_loop = ThreadJob(self.make_iteration, 0.25)
        self.game_loop.start()

    def stop(self):
        self.game_loop.stop()
        self.enemy_positions_changed_listener = lambda x: x

    def make_iteration(self):
        new_enemy_positions = []
        for enemy_position in self.enemy_positions:
            new_enemy_positions.append(self.enemy_behaviour.get_next_position(enemy_position.x, enemy_position.y))
        self.enemy_positions = new_enemy_positions
        self.enemy_positions_changed_listener(self.enemy_positions)

    def set_player_position(self, x, y):
        self.player_position = Position(x, y)
        for enemy_position in self.enemy_positions:
            if enemy_position.x == x and enemy_position.y == y:
                self.game_over_lister()
                return
