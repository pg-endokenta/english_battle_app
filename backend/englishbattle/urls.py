from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_session, name='create_session'),
    path('join/<uuid:session_id>/', views.join_session, name='join_session'),
    path('quiz/<uuid:session_id>/', views.quiz, name='quiz'),
    path('results/<uuid:session_id>/', views.results, name='results'),
    path('sessions/', views.available_sessions, name='available_sessions'),
    path('home/', views.home, name='home'),
    path('sentences/', views.sentence_list, name='sentence_list'),
]
