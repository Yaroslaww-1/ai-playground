import random

from domain.character import Character
from domain.direction_enum import Direction
from domain.direction_helper import DirectionHelper
from domain.position import Position
from domain.search.search import Search
from domain.search.search_algorithm_enum import SearchAlgorithm


class Player(Character):
    def __init__(self, map, initial_x, initial_y, on_move):
        super().__init__(map, initial_x, initial_y)
        self.map = map
        self.on_move = on_move
        self.is_moving = True
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.direction = Direction.RIGHT
        self.search = Search(map)
        self.paths_to_enemies = []

    def set_position(self, position):
        self.x = position.x
        self.y = position.y
        self.on_move()

    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.direction = Direction.RIGHT

    def calculate_paths_to_enemies(self, enemies, search_algorithm):
        self.paths_to_enemies.clear()
        if search_algorithm == SearchAlgorithm.BFS:
            for enemy in enemies:
                self.paths_to_enemies += self.search.bfs(Position(self.x, self.y), Position(enemy.x, enemy.y))

        if search_algorithm == SearchAlgorithm.DFS:
            for enemy in enemies:
                self.paths_to_enemies += self.search.dfs(Position(self.x, self.y), Position(enemy.x, enemy.y))

        if search_algorithm == SearchAlgorithm.UCS:
            for enemy in enemies:
                self.paths_to_enemies += self.search.ucs(Position(self.x, self.y), Position(enemy.x, enemy.y))

    def get_next_position(self):
        if self.is_moving and self.can_move_in_direction():
            new_position = self.map.get_next_position_in_direction(self.x, self.y, self.direction)
            return new_position
        else:
            return Position(self.x, self.y)

    def move_to_next_position(self):
        next_position = self.get_next_position()
        self.set_position(next_position)
