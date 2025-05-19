from django.urls import path
from . import views

urlpatterns = [
    path('practice/', views.react_index, name='practice'),
    path('practice/stats', views.react_index, name='react_practice_stats'),
]