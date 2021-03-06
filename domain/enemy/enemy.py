from domain.character import Character
from domain.direction_enum import Direction
from domain.player.player import Player
from domain.position import Position


class Enemy(Character):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)
        self.previous_position = None

    def get_next_direction(self, player) -> Direction:
        raise NotImplementedError()

    def move_to_next_position(self, player: Player):
        next_position = self.get_next_position()
        self.previous_position = Position(self.x, self.y)
        self.set_position(next_position)
        self.direction = self.get_next_direction(player)
