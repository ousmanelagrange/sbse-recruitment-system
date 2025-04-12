from django.urls import path
from .views import run_genetic_algorithm

urlpatterns = [
    path('run-genetic-algorithm/', run_genetic_algorithm, name='run_genetic_algorithm'),
]