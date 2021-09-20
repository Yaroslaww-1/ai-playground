import time, threading


class ThreadJob():
    def __init__(self, interval):
        self.interval = interval
        self.action = lambda: True
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.set_interval)

    def set_interval(self):
        next_time = time.time() + self.interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.interval
            self.action()

    def start(self, action):
        self.action = action
        self.thread.start()

    def stop(self):
        self.stop_event.set()
