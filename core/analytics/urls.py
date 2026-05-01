from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.dashboard_analytics, name='analytics'),
    path('analytics/stats-rapides/', views.stats_rapides, name='stats_rapides'),
]