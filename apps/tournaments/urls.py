from django.urls import path, include
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='list'),
    path('<slug:slug>/', views.TournamentDetailView.as_view(), name='detail'),
    path('<slug:slug>/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('<slug:slug>/tab/', views.PublicTabView.as_view(), name='public_tab'),
    path('<slug:slug>/participants/', include('apps.participants.urls')),
    path('<slug:slug>/adjudication/', include('apps.adjudication.urls')),
    path('<slug:slug>/draws/', include('apps.draws.urls')),
    path('<slug:slug>/results/', include('apps.results.urls')),
]
