from typing import List

from domain.character import Character
from domain.direction_enum import Direction
from domain.position import Position
from domain.score import Score


class Player(Character):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)
        self.on_move = lambda: True

    def set_on_move(self, on_move):
        self.on_move = on_move

    def set_position(self, position):
        self.x = position.x
        self.y = position.y
        self.on_move()

    def get_next_direction(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> Direction:
        raise NotImplementedError()

    def move_to_next_position(
        self,
        enemy_positions: List[Position],
        score: Score
    ) -> None:
        next_position = self.get_next_position()
        self.set_position(next_position)
        self.direction = self.get_next_direction(enemy_positions, score)
