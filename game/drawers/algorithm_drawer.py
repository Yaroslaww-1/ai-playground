from domain.search.search_algorithm_enum import SearchAlgorithm
from game.game_settings import UNIT_IN_PX


class AlgorithmDrawer:
    def __init__(self, draw_helper):
        self.draw_helper = draw_helper

    def draw_algorithm_info(self, game):
        algorithm = ''
        if game.search_algorithm == SearchAlgorithm.BFS:
            algorithm = 'BFS'
        if game.search_algorithm == SearchAlgorithm.DFS:
            algorithm = 'DFS'
        if game.search_algorithm == SearchAlgorithm.UCS:
            algorithm = 'UCS'
        time = game.player.search.last_search_time
        self.draw_helper.draw_text(0, game.map.height * UNIT_IN_PX - 50, f'Algorithm: {algorithm} Time: {time}ms')

    def draw_path(self, player):
        for path in player.paths_to_enemies:
            self.draw_helper.draw_path_tile(path.x, path.y)
