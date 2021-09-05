from pacman.domain.position import Position


class Game:
    def __init__(self, map, enemy_count=3):
        self.map = map
        self.enemy_count = enemy_count
        self.player_position = self.get_initial_player_position()
        self.enemy_positions = self.get_initial_enemies_position()

    def get_initial_player_position(self):
        return Position(0, 0)

    def get_initial_enemies_position(self):
        enemy_positions = []
        for i in range(self.enemy_count):
            # always locate enemies at the last column
            x = self.map.width - 1
            y = self.map.height - 1 - i
            enemy_positions.append(Position(x, y))
        return enemy_positions
