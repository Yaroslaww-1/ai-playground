from django.urls import path
from django.conf.urls import url

from pacman.consumers import PacmanConsumer

websocket_urlpatterns = [
    url(r'^ws/game/$', PacmanConsumer.as_asgi())
]
