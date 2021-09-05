from django.urls import path

from . import views

urlpatterns = [
    path('map', views.get_map, name='get_map'),
    path('game/start', views.start_game, name='start_game'),
]