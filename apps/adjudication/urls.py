from django.urls import path
from . import views

app_name = 'adjudication'

urlpatterns = [
    path('', views.AdjudicatorListView.as_view(), name='list'),
    path('<int:adj_id>/', views.AdjudicatorDetailView.as_view(), name='detail'),
]
