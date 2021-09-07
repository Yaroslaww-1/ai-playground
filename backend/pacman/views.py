import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

from pacman.domain.game import Game
from pacman.domain.map import Map
from pacman.domain.map_filler import MapFiller
from pacman.game_settings import GAME_LOOP_INTERVAL
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
    game = Game(map, GAME_LOOP_INTERVAL)
    if AppState.game:
        AppState.game.stop()
    AppState.set_game(game)

    return JsonResponse(GameSerializer.to_json(game))
