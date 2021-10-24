from pygame import display


class GameDrawer:
    def __init__(self, map_drawer, enemy_drawers, player_drawer, score_drawer):
        self.map_drawer = map_drawer
        self.enemy_drawers = enemy_drawers
        self.player_drawer = player_drawer
        self.score_drawer = score_drawer

    def draw_game(self, game, ticks):
        self.map_drawer.draw_map(game.map)

        if not game.is_game_running:
            ticks = 0

        for enemy_drawer in self.enemy_drawers:
            enemy_drawer.draw_enemy(ticks)

        self.player_drawer.draw_player(ticks)

        if game.is_game_over:
            self.score_drawer.draw_game_over(game)
        else:
            self.score_drawer.draw_score(game)

        display.update()
