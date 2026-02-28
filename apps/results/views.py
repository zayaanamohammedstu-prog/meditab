from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from apps.tournaments.models import Tournament
from apps.draws.models import Debate
from apps.participants.models import Team, Speaker
from .models import Ballot, TeamResult, SpeakerResult


class BallotEntryView(LoginRequiredMixin, View):
    template_name = 'results/ballot_entry.html'

    def get(self, request, slug, debate_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        debate = get_object_or_404(Debate, id=debate_id, round__tournament=tournament)
        teams = [
            (debate.og_team, 'OG'),
            (debate.oo_team, 'OO'),
            (debate.cg_team, 'CG'),
            (debate.co_team, 'CO'),
        ]
        context = {
            'tournament': tournament,
            'debate': debate,
            'teams': [(t, pos) for t, pos in teams if t],
        }
        return render(request, self.template_name, context)

    def post(self, request, slug, debate_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        debate = get_object_or_404(Debate, id=debate_id, round__tournament=tournament)

        ballot = Ballot.objects.create(debate=debate)

        positions = ['OG', 'OO', 'CG', 'CO']
        teams_map = {
            'OG': debate.og_team,
            'OO': debate.oo_team,
            'CG': debate.cg_team,
            'CO': debate.co_team,
        }
        # BP points: 1st=3, 2nd=2, 3rd=1, 4th=0
        points_map = {1: 3, 2: 2, 3: 1, 4: 0}

        for pos in positions:
            team = teams_map.get(pos)
            if not team:
                continue
            rank_str = request.POST.get(f'rank_{pos}', '')
            try:
                rank = int(rank_str)
            except (ValueError, TypeError):
                continue
            pts = points_map.get(rank, 0)
            TeamResult.objects.create(
                ballot=ballot,
                team=team,
                position=pos,
                rank=rank,
                total_points=pts,
            )

        # Speaker scores
        for pos in positions:
            team = teams_map.get(pos)
            if not team:
                continue
            for speaker in team.speakers.all():
                score_str = request.POST.get(f'score_{speaker.id}', '')
                try:
                    score = float(score_str)
                except (ValueError, TypeError):
                    score = 0.0
                SpeakerResult.objects.create(ballot=ballot, speaker=speaker, score=score)

        messages.success(request, 'Ballot submitted successfully.')
        return redirect('tournaments:detail', slug=slug)


class ConfirmBallotView(LoginRequiredMixin, View):
    def post(self, request, slug, ballot_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        ballot = get_object_or_404(Ballot, id=ballot_id, debate__round__tournament=tournament)
        ballot.confirmed = True
        ballot.save()
        messages.success(request, 'Ballot confirmed.')
        return redirect('tournaments:admin_dashboard', slug=slug)


class ResultsView(View):
    template_name = 'results/results.html'

    def get(self, request, slug):
        tournament = get_object_or_404(Tournament, slug=slug)
        from apps.draws.models import Round
        rounds = Round.objects.filter(tournament=tournament).order_by('seq')
        context = {
            'tournament': tournament,
            'rounds': rounds,
        }
        return render(request, self.template_name, context)
