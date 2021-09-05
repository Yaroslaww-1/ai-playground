from django.urls import path

from . import views

urlpatterns = [
    path('map', views.get_map, name='get_map'),
]