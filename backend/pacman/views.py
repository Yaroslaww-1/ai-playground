import json
from django.http import JsonResponse

from pacman.domain.game import Game
from pacman.domain.map import Map
from pacman.domain.map_filler import MapFiller
from pacman.serializers import GameSerializer, MapSerializer


def get_map(request):
    map = Map(16, 16)
    map_filler = MapFiller(map)
    map_filler.fill()
    return JsonResponse(MapSerializer.to_json(map))


def get_game(request):
    map = Map(16, 16)
    map_filler = MapFiller(map)
    map_filler.fill()
    game = Game(map)
    print(type(game))
    return JsonResponse(GameSerializer.to_json(game))
