from json import JSONEncoder


class PositionSerializer():
    @staticmethod
    def to_json(position):
        return {
            'x': position.x,
            'y': position.y,
        }


class MapSerializer():
    @staticmethod
    def to_json(map):
        return {
            'tiles': map.tiles,
            'width': map.width,
            'height': map.height,
        }


class ScoreSerializer():
    @staticmethod
    def to_json(score):
        return {
            'score': score.score,
            'availablePoints': list(map(PositionSerializer.to_json, score.available_points)),
        }


class EnemySerializer():
    @staticmethod
    def to_json(enemy):
        return {
            'x': enemy.x,
            'y': enemy.y
        }


class GameSerializer():
    @staticmethod
    def to_json(game):
        return {
            'map': MapSerializer.to_json(game.map),
            'enemyCount': game.enemy_count,
            'playerPosition': PositionSerializer.to_json(game.player_position),
            'enemyPositions': list(map(EnemySerializer.to_json, game.enemies)),
        }