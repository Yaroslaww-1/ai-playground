from domain.enemy.enemy import Enemy
from domain.position import Position
from domain.search.search_algorithm import SearchAlgorithm


class EnemySearchAlgorithm(Enemy):
    def __init__(self, map, initial_x, initial_y, search_algorithm: SearchAlgorithm):
        super().__init__(map, initial_x, initial_y)
        self.search_algorithm = search_algorithm
        self.previous_position = None

    def get_next_direction(self, player):
        previous_position = self.map.get_next_position_in_direction(self.x, self.y, self.map.get_reverse_direction(self.direction))
        optimal_path = self.search_algorithm.find_path(
            Position(self.x, self.y),
            Position(player.x, player.y),
            [],
            self.previous_position
        )
        for next_position in optimal_path:
            if next_position.x != self.x or next_position.y != self.y:
                return self.map.get_direction_from_to_positions(self.x, self.y, next_position.x, next_position.y)
        return None

    def move_to_next_position(self, player):
        # should_decide_direction = self.map.get_next_position_in_direction(self.x, self.y, self.direction) is None
        # if should_decide_direction:
        next_position = self.get_next_position()
        print(f"pos {self.previous_position} -> {self.x}-{self.y} -> {next_position} {self.direction}")
        self.previous_position = Position(self.x, self.y)
        self.set_position(next_position)
        self.direction = self.get_next_direction(player)
        # else:
        #     self.set_position(self.map.get_next_position_in_direction(self.x, self.y, self.direction))
