from domain.enemy import Enemy
from domain.position import Position
from domain.lib.thread_job import ThreadJob
from domain.score import Score


class Game:
    def __init__(self, map, game_loop_interval, enemy_count=3):
        self.map = map
        self.enemy_count = enemy_count
        self.player_position = self.get_initial_player_position()
        self.enemies = self.get_initial_enemies()
        self.game_loop = None
        self.enemy_positions_changed_listener = lambda x: x
        self.game_over_lister = None
        self.score = None
        self.game_loop_interval = game_loop_interval

    def get_initial_player_position(self):
        return Position(0, 0)

    def get_initial_enemies(self):
        enemies = []
        for i in range(self.enemy_count):
            # always locate enemies at the last column
            x = self.map.width - 1
            y = self.map.height - 1 - i
            enemy = Enemy(self.map, x, y)
            enemies.append(enemy)
        return enemies

    def start(self, enemy_positions_changed_listener, game_over_lister, score_changed_listener):
        self.enemy_positions_changed_listener = enemy_positions_changed_listener
        self.game_over_lister = game_over_lister
        self.score = Score(self.map, score_changed_listener)

        self.game_loop = ThreadJob(self.make_iteration, self.game_loop_interval)
        self.game_loop.start()

    def stop(self):
        self.game_loop.stop()
        self.enemy_positions_changed_listener = lambda x: x
        self.game_over_lister = None
        self.player_position = self.get_initial_player_position()
        self.enemies = self.get_initial_enemies()

    def make_iteration(self):
        for enemy in self.enemies:
            enemy.move_to_next_position()
        self.enemy_positions_changed_listener(self.enemies)
        self.check_if_game_over()

    def set_player_position(self, x, y):
        self.player_position = Position(x, y)
        self.score.handle_player_move(self.player_position)
        self.check_if_game_over()

    def check_if_game_over(self):
        for enemy in self.enemies:
            enemy_position = enemy.get_position()
            if enemy_position.x == self.player_position.x and enemy_position.y == self.player_position.y:
                self.game_over_lister()
                return
