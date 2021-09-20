from pygame import display


class GameDrawer:
    def __init__(self, map_drawer, enemy_drawers, player_drawer, score_drawer):
        self.map_drawer = map_drawer
        self.enemy_drawers = enemy_drawers
        self.player_drawer = player_drawer
        self.score_drawer = score_drawer

    def draw_game(self, game, ticks):
        self.map_drawer.draw_map(game.map)
        for enemy_drawer in self.enemy_drawers:
            enemy_drawer.draw_enemy(ticks)
        self.player_drawer.draw_player(ticks)
        self.score_drawer.draw_score()
        display.update()
