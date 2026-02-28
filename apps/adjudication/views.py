from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.tournaments.models import Tournament
from .models import Adjudicator


class AdjudicatorListView(View):
    template_name = 'adjudication/list.html'

    def get(self, request, slug):
        tournament = get_object_or_404(Tournament, slug=slug)
        adjudicators = Adjudicator.objects.filter(tournament=tournament).select_related('institution')
        context = {
            'tournament': tournament,
            'adjudicators': adjudicators,
        }
        return render(request, self.template_name, context)


class AdjudicatorDetailView(View):
    template_name = 'adjudication/detail.html'

    def get(self, request, slug, adj_id):
        tournament = get_object_or_404(Tournament, slug=slug)
        adjudicator = get_object_or_404(Adjudicator, id=adj_id, tournament=tournament)
        feedback = adjudicator.feedback_received.select_related('debate__round', 'source_adjudicator')
        context = {
            'tournament': tournament,
            'adjudicator': adjudicator,
            'feedback': feedback,
        }
        return render(request, self.template_name, context)
