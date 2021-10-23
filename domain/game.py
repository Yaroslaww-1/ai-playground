from typing import List

from domain.enemy.enemy import Enemy
from domain.player.player import Player
from domain.position import Position
from domain.score import Score


class Game:
    def __init__(self, map, game_loop, player: Player, enemies: List[Enemy]):
        self.map = map
        self.player = player
        self.player.set_on_move(self.handle_player_move)
        self.game_loop = None
        self.enemies = enemies
        self.score = Score(self.map)
        self.game_loop = game_loop
        self.is_game_running = False
        self.is_game_over = False
        self.on_iteration = lambda: True
        self.game_tick = 0

    def start(self):
        self.player.reset_position()
        for enemy in self.enemies:
            enemy.reset_position()
        self.score.reset()
        self.is_game_running = True
        self.is_game_over = False
        self.game_tick = 0

    def stop(self):
        self.game_loop.stop()
        self.is_game_running = False

    def make_iteration(self):
        if not self.is_game_running:
            return
        if self.game_tick % 2 == 0:
            for enemy in self.enemies:
                enemy.move_to_next_position(self.player)
        self.player.move_to_next_position(list(map(lambda enemy: Position(enemy.x, enemy.y), self.enemies)), self.score)
        self.check_if_game_over()
        self.game_tick += 1

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
