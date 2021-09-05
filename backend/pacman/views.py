import json
from django.http import JsonResponse

from pacman.domain.map import Map
from pacman.domain.map_filler import MapFiller


def get_map(request):
    map = Map(16, 16)
    map_filler = MapFiller(map)
    map_filler.fill()
    return JsonResponse({'map': map.tiles})
