from django.urls import path

from .views import index,movies

urlpatterns = [
    path('', index, name='index'),
    path('movies', movies, name='movies'),
]