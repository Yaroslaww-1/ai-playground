import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

from pacman.domain.enemy_behavior_random import EnemyBehaviourRandom
from pacman.domain.game import Game
from pacman.domain.map import Map
from pacman.domain.map_filler import MapFiller
from pacman.serializers import GameSerializer, MapSerializer
from pacman.app_state import AppState


def get_map(request):
    map = Map(16, 16)
    map_filler = MapFiller(map)
    map_filler.fill()
    return JsonResponse(MapSerializer.to_json(map))


@api_view(['POST'])
def start_game(request):
    # Map initialization
    map = Map(16, 16)
    map_filler = MapFiller(map)
    map_filler.fill()
    # Game initialization
    game = Game(map, EnemyBehaviourRandom(map))
    AppState.set_game(game)

    return JsonResponse(GameSerializer.to_json(game))
