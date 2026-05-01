from django.urls import path
from django.conf.urls.static import static
from core import settings

# Importation segmentée des vues
from . import views           # Principal (Core & Dashboard)
from . import views_design    # Design & Customizer
from . import views_demo      # Galerie & Aperçus
from . import views_content   # CRUD Contenu, Avis & Messages

app_name = 'portfolio'

urlpatterns = [
    # ==========================================================
    # 1. CŒUR DU SYSTÈME (Views Principal)
    # ==========================================================
    path('portfolio/', views.dashboard_portfolio, name='dashboard_portfolio'),
    path('portfolio/creer/', views.creer_portfolio, name='creer_portfolio'),
    path('portfolio/detail/', views.portfolio_detail, name='portfolio_detail'),
    path('modifier/', views.modifier_infos, name='modifier_infos'),
    path('p/preview/<slug:slug>/', views.portfolio_public, name='portfolio_public_preview'),

    # ==========================================================
    # 2. DESIGN & PERSONNALISATION (Views Design)
    # ==========================================================
    path('portfolio/customizer/', views_design.customizer, name='customizer'),
    path('portfolio/tokens/', views_design.sauvegarder_tokens, name='sauvegarder_tokens'),
    path('portfolio/palette/<str:nom_palette>/', views_design.appliquer_palette, name='appliquer_palette'),
    path('changer-template/', views_design.changer_template, name='changer_template'),
    path('appliquer/<str:template_slug>/', views_design.appliquer_et_customiser, name='appliquer_et_customiser'),
    path('portfolio/modifier/', views_design.modifier_portfolio, name='modifier_portfolio'),

    # ==========================================================
    # 3. GALERIE & DÉMONSTRATION (Views Demo)
    # ==========================================================
    path('template/liste/', views_demo.template_list, name='template_list'),
    path('template/<slug:slug>/', views_demo.template_detail, name='template_detail'),
    path('template/<slug:slug>/demo/', views_demo.portfolio_demo, name='portfolio_demo'),
    path('template/<slug:slug>/apercu/', views_demo.portfolio_demo_apercu, name='portfolio_demo_apercu'),

    # ==========================================================
    # 4. GESTION DU CONTENU (Views Content)
    # ==========================================================
    # --- Réalisations ---
    path('portfolio/realisations/ajouter/', views_content.ajouter_realisation, name='ajouter_realisation'),
    path('realisation/modifier/<int:pk>/', views_content.modifier_realisation, name='modifier_realisation'),
    path('portfolio/realisations/supprimer/<int:pk>/', views_content.supprimer_realisation, name='supprimer_realisation'),

    # --- Services ---
    path('service/ajouter/', views_content.ajouter_service, name='ajouter_service'),
    path('service/modifier/<int:pk>/', views_content.modifier_service, name='modifier_service'),
    path('service/supprimer/<int:pk>/', views_content.supprimer_service, name='supprimer_service'),

    # --- Statistiques ---
    path('portfolio/statistiques/ajouter/', views_content.ajouter_stat, name='ajouter_statistique'),
    path('portfolio/statistiques/gerer/<int:pk>/', views_content.gerer_statistique, name='gerer_statistique'), # Ajouté pour la cohérence
    path('portfolio/statistiques/supprimer/<int:pk>/', views_content.supprimer_stat, name='supprimer_stat'),

    # --- Réseaux Sociaux ---
    path('portfolio/reseaux/modifier/', views_content.modifier_reseaux, name='modifier_reseaux'),

    # --- Témoignages (Avis) ---
    path('avis/public/<slug:slug>/', views_content.laisser_avis_public, name='laisser_avis_public'),
    # path('dashboard/temoignages/ajouter/', views_content.ajouter_temoignage_dash, name='ajouter_temoignage'),
    path('portfolio/temoignages/approuver/<int:pk>/', views_content.approuver_temoignage, name='approuver_temoignage'),
    path('portfolio/temoignages/supprimer/<int:pk>/', views_content.supprimer_temoignage, name='supprimer_temoignage'),

    # --- Messagerie ---
    path('dashboard/messages/', views_content.messages_recus, name='messages_recus'),
    path('envoi/message/<slug:slug>/', views_content.envoyer_message, name='envoyer_message'),
    path('marquer/message/<int:pk>/', views_content.marquer_lu_message, name='marquer_lu_message'),
    path('messages/supprimer/<int:pk>/', views_content.supprimer_message, name='supprimer_message'),
]

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)