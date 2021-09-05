import json
from django.http import JsonResponse

from pacman.domain.map_generator import MapGenerator


def get_map(request):
    generator = MapGenerator(16, 16)
    map = generator.generate()
    print(map)
    return JsonResponse({'map': map})
