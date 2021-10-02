import random

from domain.character import Character
from domain.direction_helper import DirectionHelper
from domain.position import Position
from domain.search.search import Search


class Enemy(Character):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)
        self.map = map
        self.direction = self.map.get_all_opened_directions(initial_x, initial_y)[0]
        self.steps_from_previous_turn = 0
        self.id = random.randint(0, 1000000)
        self.is_moving = True
        self.search = Search(map)

    def get_next_direction(self, player):
        path_to_player = self.search.bfs(Position(self.x, self.y), Position(player.x, player.y))
        for next_position in path_to_player:
            if next_position.x != self.x or next_position.y != self.y:
                return self.map.get_direction_from_to_positions(self.x, self.y, next_position.x, next_position.y)
        return None

    def get_next_position(self):
        if self.is_moving and self.can_move_in_direction():
            new_position = self.map.get_next_position_in_direction(self.x, self.y, self.direction)
            return new_position
        else:
            return Position(self.x, self.y)

    def move_to_next_position(self, player):
        next_position = self.get_next_position()
        self.set_position(next_position)
        self.direction = self.get_next_direction(player)
