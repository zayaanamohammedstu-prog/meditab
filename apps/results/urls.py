from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('ballot/<int:debate_id>/', views.BallotEntryView.as_view(), name='ballot_entry'),
    path('ballot/confirm/<int:ballot_id>/', views.ConfirmBallotView.as_view(), name='confirm_ballot'),
    path('', views.ResultsView.as_view(), name='results'),
]
