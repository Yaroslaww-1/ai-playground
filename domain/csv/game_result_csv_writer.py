from sys import path


class GameResultCsvWriter:
    def __init__(self, file_path: path):
        self.file_path = file_path

    def write(self, win: bool, time, points: int, algorithm: str):
        with open(self.file_path, 'a') as f:
            row = [str(win), str(time), str(points), algorithm]
            f.write(','.join(row) + '\n')