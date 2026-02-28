from django.contrib import admin
from .models import Ballot, TeamResult, SpeakerResult


@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ('id', 'debate', 'adjudicator', 'confirmed', 'discarded', 'submitted_at')
    list_filter = ('confirmed', 'discarded')


@admin.register(TeamResult)
class TeamResultAdmin(admin.ModelAdmin):
    list_display = ('team', 'position', 'rank', 'total_points', 'ballot')
    list_filter = ('position', 'rank')


@admin.register(SpeakerResult)
class SpeakerResultAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'score', 'position_in_team', 'ballot')
