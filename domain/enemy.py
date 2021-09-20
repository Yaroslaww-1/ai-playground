import random

from domain.character import Character
from domain.direction_helper import DirectionHelper
from domain.position import Position


class Enemy(Character):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)
        self.map = map
        self.direction = self.map.get_all_opened_directions(initial_x, initial_y)[0]
        self.steps_from_previous_turn = 0
        self.id = random.randint(0, 1000000)
        self.is_moving = True

    def get_next_position(self):
        next_position = self.map.get_next_position_in_direction(self.x, self.y, self.direction)

        self.steps_from_previous_turn += 1

        should_try_to_turn = self.steps_from_previous_turn > 10
        if should_try_to_turn:
            turn_direction = self.get_turn_direction()
            if turn_direction is not None:
                self.steps_from_previous_turn = 0
                self.direction = turn_direction

        opened_directions = self.map.get_all_opened_directions(next_position.x, next_position.y)
        if self.direction not in opened_directions:
            self.direction = opened_directions[0]

        return next_position

    def get_turn_direction(self):
        opened_directions = self.map.get_all_opened_directions(self.x, self.y)
        for opened_direction in opened_directions:
            if opened_direction == self.direction:
                continue
            if DirectionHelper.is_directions_reverse(self.direction, opened_direction) is False:
                return opened_direction
        return None
