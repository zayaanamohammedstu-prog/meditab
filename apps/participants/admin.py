from django.contrib import admin
from .models import Institution, Team, Speaker


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'region')
    search_fields = ('name', 'code')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'institution', 'tournament', 'created_at')
    list_filter = ('tournament', 'institution')
    search_fields = ('name', 'code_name')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'institution', 'email')
    list_filter = ('team__tournament',)
    search_fields = ('name', 'email')
