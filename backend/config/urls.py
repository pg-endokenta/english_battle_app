from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home')),
    path('', include('englishbattle.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')), 
    # for api
    path('api/', include('englishbattle.urls_api')),
    path('api/', include('books.urls_api')),
]
