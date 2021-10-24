from domain.enemy.enemy import Enemy
from domain.search.search_algorithm import SearchAlgorithm


class EnemyRandom(Enemy):
    def __init__(self, map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)

    def get_next_direction(self, player):
        return self.map.get_random_opened_direction(self.x, self.y)

    def move_to_next_position(self, player):
        next_position = self.get_next_position()
        self.set_position(next_position)
        self.direction = self.get_next_direction(player)
