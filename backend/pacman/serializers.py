from json import JSONEncoder


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
            'playerPosition': game.player_position,
            'enemyPositions': game.enemy_positions,
        }