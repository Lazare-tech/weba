from django.urls import path
from . import views

urlpatterns = [
    path('tarification/', views.tarification, name='tarification'),
    path('upgrade/<str:nom_plan>/', views.demander_upgrade, name='demander_upgrade'),
    path('activer/<int:user_id>/<str:nom_plan>/', views.activer_plan, name='activer_plan'),
    path('admin/demandes/', views.admin_demandes, name='admin_demandes'),
]