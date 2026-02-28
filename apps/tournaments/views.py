from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count, Avg
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Tournament
from apps.participants.models import Team, Speaker
from apps.adjudication.models import Adjudicator
from apps.draws.models import Round, Debate
from apps.results.models import TeamResult, SpeakerResult


class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/list.html'
    context_object_name = 'tournaments'
    queryset = Tournament.objects.all()


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = self.object
        context['teams_count'] = t.teams.count()
        context['adjudicators_count'] = t.adjudicators.count()
        context['rounds'] = t.rounds.order_by('seq')
        context['rounds_count'] = t.rounds.count()
        return context


class AdminDashboardView(LoginRequiredMixin, View):
    template_name = 'tournaments/admin_dashboard.html'

    def get(self, request, slug):
        tournament = get_object_or_404(Tournament, slug=slug)
        teams = Team.objects.filter(tournament=tournament).select_related('institution')
        adjudicators = Adjudicator.objects.filter(tournament=tournament).select_related('institution')
        rounds = Round.objects.filter(tournament=tournament).order_by('seq')
        context = {
            'tournament': tournament,
            'teams': teams,
            'adjudicators': adjudicators,
            'rounds': rounds,
            'teams_count': teams.count(),
            'adjudicators_count': adjudicators.count(),
            'rounds_count': rounds.count(),
        }
        return render(request, self.template_name, context)


class PublicTabView(View):
    template_name = 'tournaments/public_tab.html'

    def get(self, request, slug):
        tournament = get_object_or_404(Tournament, slug=slug)

        # Build team standings from confirmed ballots
        teams = Team.objects.filter(tournament=tournament).select_related('institution')
        team_standings = []
        for team in teams:
            results = TeamResult.objects.filter(team=team, ballot__confirmed=True)
            total_pts = sum(r.total_points for r in results)
            wins = results.filter(rank=1).count()
            team_standings.append({
                'team': team,
                'total_points': total_pts,
                'wins': wins,
                'debates': results.count(),
            })
        team_standings.sort(key=lambda x: (-x['wins'], -x['total_points']))
        for i, ts in enumerate(team_standings, 1):
            ts['rank'] = i

        # Build speaker standings from confirmed ballots
        from apps.participants.models import Speaker
        speakers = Speaker.objects.filter(team__tournament=tournament).select_related('team', 'institution')
        speaker_standings = []
        for speaker in speakers:
            results = SpeakerResult.objects.filter(speaker=speaker, ballot__confirmed=True)
            total_score = sum(r.score for r in results)
            count = results.count()
            avg_score = (total_score / count) if count > 0 else 0
            speaker_standings.append({
                'speaker': speaker,
                'total_score': total_score,
                'avg_score': round(avg_score, 2),
                'speeches': count,
            })
        speaker_standings.sort(key=lambda x: -x['total_score'])
        for i, ss in enumerate(speaker_standings, 1):
            ss['rank'] = i

        context = {
            'tournament': tournament,
            'team_standings': team_standings,
            'speaker_standings': speaker_standings,
        }
        return render(request, self.template_name, context)
