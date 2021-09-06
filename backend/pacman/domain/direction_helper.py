import random

from pacman.domain.direction_enum import Direction


class DirectionHelper:
    @staticmethod
    def get_random_directions():
        directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        random.shuffle(directions)
        return directions

    @staticmethod
    def is_directions_reverse(direction1, direction2):
        return (direction1 + direction2) % 2 == 1
