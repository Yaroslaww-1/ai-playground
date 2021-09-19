import pygame.time


class GameLoop:
    def __init__(self, game_loop_interval):
        self.is_running = False
        self.game_loop_interval = game_loop_interval

    def start(self, make_iteration):
        self.is_running = True
        while self.is_running:
            pygame.time.delay(self.game_loop_interval)
            make_iteration()

    def stop(self):
        self.is_running = False
