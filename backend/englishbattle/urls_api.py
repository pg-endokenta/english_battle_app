# urls.py
from django.urls import path, include
from .views_api import random_sentence
from rest_framework.routers import DefaultRouter
from .views_api import PracticeRecordViewSet, practice_stats

router = DefaultRouter()
router.register(r'practice-records', PracticeRecordViewSet, basename='practice-record')

urlpatterns = [
    path('sentences/random/', random_sentence),
    path('', include(router.urls)),
    path('practice-stats/', practice_stats, name='practice-stats'),
]
