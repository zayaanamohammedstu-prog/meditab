from django.urls import path
from . import views

app_name = 'participants'

urlpatterns = [
    path('teams/<int:team_id>/', views.TeamDashboardView.as_view(), name='team_dashboard'),
    path('speakers/<int:speaker_id>/', views.SpeakerProfileView.as_view(), name='speaker_profile'),
]
