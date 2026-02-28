from django.urls import path
from . import views

app_name = 'draws'

urlpatterns = [
    path('round/<int:round_id>/', views.RoundDrawView.as_view(), name='round_draw'),
    path('round/<int:round_id>/generate/', views.GenerateDrawView.as_view(), name='generate_draw'),
    path('round/<int:round_id>/release/', views.ReleaseDrawView.as_view(), name='release_draw'),
]
