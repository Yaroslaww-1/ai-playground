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


class GameSerializer():
    @staticmethod
    def to_json(game):
        return {
            'map': MapSerializer.to_json(game.map),
            'enemyCount': game.enemy_count,
            'playerPosition': PositionSerializer.to_json(game.player_position),
            'enemyPositions': list(map(PositionSerializer.to_json, game.enemy_positions)),
        }