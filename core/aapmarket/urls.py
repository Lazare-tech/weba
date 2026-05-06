from django.urls import path
from django.views.generic import TemplateView, ListView
from . import views

# Définition du namespace pour faciliter les liens dans les templates (ex: {% url 'aapmarket:tarifs' %})
app_name = 'aapmarket'
urlpatterns = [
    # --- Plateforme ---
    path('', views.TemplatesView.as_view(), name='index'),
    path('moteur-de-blog/', views.BlogEngineView.as_view(), name='blog_engine'),
    path('tarifs/', views.TarifsView.as_view(), name='tarifs'),
    path('demo/', views.DemoView.as_view(), name='demo'),

    # --- Entreprise ---
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/detail/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('a-propos/', views.AProposView.as_view(), name='a_propos'),
    path('accelerateur/', views.AccelerateurView.as_view(), name='accelerateur'),
    path('carrieres/', views.CareersView.as_view(), name='careers'),
    path('presse/', views.PressView.as_view(), name='press'),

    # --- Support & Légal ---
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('mentions-legales/', views.LegalView.as_view(), name='legal'),
    path('confidentialite/', views.PrivacyView.as_view(), name='privacy'),
]