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
            'enemy_count': game.enemy_count,
            'player_position': game.player_position,
            'enemy_positions': game.enemy_positions,
        }