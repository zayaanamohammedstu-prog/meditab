from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from apps.tournaments.models import Tournament
from apps.results.models import TeamResult, SpeakerResult
from .models import Team, Speaker


class TeamDashboardView(View):
    template_name = 'participants/team_dashboard.html'

    def get(self, request, slug, team_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        team = get_object_or_404(Team, id=team_id, tournament=tournament)
        results = TeamResult.objects.filter(
            team=team, ballot__confirmed=True
        ).select_related('ballot__debate__round', 'ballot__debate__room').order_by(
            'ballot__debate__round__seq'
        )
        speakers = team.speakers.all()
        context = {
            'tournament': tournament,
            'team': team,
            'results': results,
            'speakers': speakers,
        }
        return render(request, self.template_name, context)


class SpeakerProfileView(View):
    template_name = 'participants/speaker_profile.html'

    def get(self, request, slug, speaker_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        speaker = get_object_or_404(Speaker, id=speaker_id, team__tournament=tournament)
        results = SpeakerResult.objects.filter(
            speaker=speaker, ballot__confirmed=True
        ).select_related('ballot__debate__round').order_by('ballot__debate__round__seq')
        context = {
            'tournament': tournament,
            'speaker': speaker,
            'results': results,
        }
        return render(request, self.template_name, context)
