from pacman.domain.position import Position


class EnemyBehaviourRandom:
    def __init__(self, map):
        self.map = map

    def get_next_position(self, current_x, current_y):
        new_position = self.map.get_random_adjacent_position(current_x, current_y)
        if new_position is None:
            return Position(current_x, current_y)
        else:
            return Position(new_position.x, new_position.y)