from django.contrib import admin
from django.urls import path, include
from apps.tournaments.views import TournamentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('tournaments/', include('apps.tournaments.urls')),
    path('', TournamentListView.as_view(), name='home'),
]
