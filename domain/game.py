from typing import Callable

from domain.enemy import Enemy
from domain.player import Player
from domain.position import Position
from domain.lib.thread_job import ThreadJob
from domain.score import Score


class Game:
    def __init__(self, map, game_loop, enemy_count=3):
        self.map = map
        self.enemy_count = enemy_count
        self.player = Player(
            map,
            self.get_initial_player_position().x,
            self.get_initial_player_position().y,
            self.handle_player_move
        )
        self.enemies = self.get_initial_enemies()
        self.game_loop = None
        self.score = Score(self.map)
        self.game_loop = game_loop
        self.is_game_running = False
        self.is_game_over = False
        self.on_iteration = lambda: True

    def get_initial_player_position(self):
        return Position(0, 0)

    def get_initial_enemies(self):
        enemies = []
        for i in range(self.enemy_count):
            # always locate enemies at the last column
            x = self.map.width - 1
            y = self.map.height - 1 - i
            enemy = Enemy(self.map, x, y)
            enemies.append(enemy)
        return enemies

    def start(self):
        self.is_game_running = True
        self.score.reset()
        self.is_game_over = False
        # self.player.set_position(self.get_initial_player_position())
        # self.enemies = self.get_initial_enemies()

    def stop(self):
        self.game_loop.stop()
        self.is_game_running = False
        self.player.reset_position()
        self.enemies = self.get_initial_enemies()

    def make_iteration(self):
        if not self.is_game_running:
            return
        for enemy in self.enemies:
            enemy.move_to_next_position()
        self.player.move_to_next_position()
        # self.notify_about_iteration()
        self.check_if_game_over()

    # def notify_about_iteration(self):
    #     self.on_iteration(self.map, self.enemies, self.score, self.is_game_running)

    def handle_player_move(self):
        if not self.is_game_running:
            return
        self.score.handle_player_move(self.player.x, self.player.y)
        self.check_if_game_over()

    def check_if_game_over(self):
        for enemy in self.enemies:
            enemy_position = enemy.get_position()
            if enemy_position.x == self.player.x and enemy_position.y == self.player.y:
                self.is_game_over = True
                self.stop()
                return

    def is_tile_without_character_or_wall(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return False
        if self.player.x == x and self.player.y == y:
            return False
        if not self.map.is_tile_empty(x, y):
            return False
        return True

    def get_characters(self):
        characters = self.enemies
        characters.append(self.player)
        return characters
