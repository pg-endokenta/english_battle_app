from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id',)
    search_fields = ('username',)
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)