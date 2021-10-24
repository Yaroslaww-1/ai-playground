from game.game_settings import UNIT_IN_PX


class ScoreDrawer:
    def __init__(self, score, drawer_helper):
        self.score = score
        self.drawer_helper = drawer_helper

    def draw_score(self, game):
        self.drawer_helper.draw_text(0, 0, f'Score: {self.score.score}')
        for available_point in self.score.available_points:
            is_tile_without_character_or_wall = game.is_tile_without_character_or_wall(available_point.x, available_point.y)
            if is_tile_without_character_or_wall:
                self.drawer_helper.draw_food(available_point.x * UNIT_IN_PX, available_point.y * UNIT_IN_PX)

    def draw_game_over(self, game):
        self.drawer_helper.draw_text(0, 0, f'Game over')