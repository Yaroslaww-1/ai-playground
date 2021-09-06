from pacman.domain.direction_helper import DirectionHelper
from pacman.domain.position import Position


class Enemy:
    def __init__(self, map, initial_x, initial_y):
        self.map = map
        self.x = initial_x
        self.y = initial_y
        self.direction = None
        self.steps_from_previous_turn = 0

    def get_next_position(self):
        opened_directions = self.map.get_all_opened_directions(self.x, self.y)

        if (self.direction is None) or (self.direction not in opened_directions):
            self.direction = opened_directions[0]

        should_try_to_turn = self.steps_from_previous_turn > 10
        if should_try_to_turn:
            turn_direction = self.get_turn_direction()
            if turn_direction is not None:
                self.steps_from_previous_turn = 0
                print("turned", self.direction, turn_direction)
                self.direction = turn_direction

        next_position = self.map.get_next_position_in_direction(self.x, self.y, self.direction)

        self.steps_from_previous_turn += 1

        return next_position

    def get_turn_direction(self):
        opened_directions = self.map.get_all_opened_directions(self.x, self.y)
        for opened_direction in opened_directions:
            if opened_direction == self.direction:
                continue
            if DirectionHelper.is_directions_reverse(self.direction, opened_direction) is False:
                return opened_direction
        return None

    def set_position(self, position):
        self.x = position.x
        self.y = position.y

    def move_to_next_position(self):
        next_position = self.get_next_position()
        self.set_position(next_position)

    def get_position(self):
        return Position(self.x, self.y)
