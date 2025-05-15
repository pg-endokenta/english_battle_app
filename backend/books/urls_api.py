from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
