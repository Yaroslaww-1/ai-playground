class AppState:
    game = None

    @staticmethod
    def set_game(game):
        AppState.game = game
