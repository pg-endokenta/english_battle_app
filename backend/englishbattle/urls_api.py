# urls.py
from django.urls import path
from .views_api import random_sentence

urlpatterns = [
    path('sentences/random/', random_sentence),
]
