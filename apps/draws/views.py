from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from apps.tournaments.models import Tournament
from .models import Round, Debate
from .pairing import generate_draw


class RoundDrawView(View):
    template_name = 'draws/round_draw.html'

    def get(self, request, slug, round_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        round_obj = get_object_or_404(Round, id=round_id, tournament=tournament)
        debates = Debate.objects.filter(round=round_obj).select_related(
            'room', 'og_team', 'oo_team', 'cg_team', 'co_team'
        ).prefetch_related('debate_adjudicators__adjudicator')
        context = {
            'tournament': tournament,
            'round': round_obj,
            'debates': debates,
        }
        return render(request, self.template_name, context)


class GenerateDrawView(LoginRequiredMixin, View):
    template_name = 'draws/generate.html'

    def get(self, request, slug, round_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        round_obj = get_object_or_404(Round, id=round_id, tournament=tournament)
        context = {'tournament': tournament, 'round': round_obj}
        return render(request, self.template_name, context)

    def post(self, request, slug, round_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        round_obj = get_object_or_404(Round, id=round_id, tournament=tournament)
        try:
            debates = generate_draw(tournament, round_obj)
            round_obj.status = Round.STATUS_CONFIRMED
            round_obj.save()
            messages.success(request, f'Draw generated: {len(debates)} debates created.')
        except Exception as e:
            messages.error(request, f'Error generating draw: {e}')
        return redirect('draws:round_draw', slug=slug, round_id=round_id)


class ReleaseDrawView(LoginRequiredMixin, View):
    def post(self, request, slug, round_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        round_obj = get_object_or_404(Round, id=round_id, tournament=tournament)
        round_obj.status = Round.STATUS_RELEASED
        round_obj.save()
        messages.success(request, f'Draw for {round_obj.name} has been released.')
        return redirect('draws:round_draw', slug=slug, round_id=round_id)
