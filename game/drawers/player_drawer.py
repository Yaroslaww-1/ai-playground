from game.drawers.character_drawer import CharacterDrawer


class PlayerDrawer(CharacterDrawer):
    def __init__(self, player, drawer_helper):
        super().__init__(player, drawer_helper)
        self.player = player
        self.drawer_helper = drawer_helper

    def draw_player(self, ticks):
        self.draw_character(ticks)
