from django.contrib import admin
from .models import Room, Round, Debate, DebateAdjudicator


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'priority')
    list_filter = ('tournament',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'seq', 'draw_type', 'status', 'is_break_round')
    list_filter = ('tournament', 'status', 'draw_type')


@admin.register(Debate)
class DebateAdmin(admin.ModelAdmin):
    list_display = ('id', 'round', 'room', 'og_team', 'oo_team', 'cg_team', 'co_team')
    list_filter = ('round__tournament',)


@admin.register(DebateAdjudicator)
class DebateAdjudicatorAdmin(admin.ModelAdmin):
    list_display = ('adjudicator', 'debate', 'adj_type')
    list_filter = ('adj_type',)
