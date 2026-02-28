from django.contrib import admin
from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'format', 'start_date', 'end_date', 'tab_released', 'registration_open')
    list_filter = ('format', 'tab_released', 'registration_open')
    search_fields = ('name', 'institution')
    prepopulated_fields = {'slug': ('name',)}
