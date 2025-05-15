from django.urls import path
from . import views
from .views import RegisterAndLoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('whoami/', views.whoami, name='whoami'),
    path('api/register/', RegisterAndLoginView.as_view(), name='register'),
    path('api/csrf/', views.csrf_token_view, name='csrf_token'),
]