from django.contrib import admin
from .models import Adjudicator, AdjudicatorConflict, AdjudicatorFeedback


@admin.register(Adjudicator)
class AdjudicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'tournament', 'base_score', 'independent')
    list_filter = ('tournament', 'independent')
    search_fields = ('name', 'email')


@admin.register(AdjudicatorConflict)
class AdjudicatorConflictAdmin(admin.ModelAdmin):
    list_display = ('adjudicator', 'team', 'conflict_type')
    list_filter = ('conflict_type',)


@admin.register(AdjudicatorFeedback)
class AdjudicatorFeedbackAdmin(admin.ModelAdmin):
    list_display = ('adjudicator', 'debate', 'score', 'submitted_at')
    list_filter = ('adjudicator',)
