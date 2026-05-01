import os
import django
from portfolio.models import Statistique
# 1. Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Verifie le nom de ton projet
django.setup()

from django.contrib.auth.models import User
from portfolio.models import (
    TemplateMetadata, CategorieTemplate, Portfolio, 
    Service, Realisation, Temoignage
)

def run_seed():
    print("🚀 Démarrage du Super Seed WEBA Africa...")

    # --- 1. CRÉATION DES CATÉGORIES ---
    categories = {
        'pro': 'Professionnel',
        'art': 'Artisanat & BTP',
        'tech': 'Technologie',
        'event': 'Événementiel'
    }
        # Stats spécifiques pour Prestige Events
    stats_prestige = [
        ('150', 'Mariages'),
        ('08', 'Pays explorés'),
        ('24k', 'Fleurs dressées'),
        ('100%', 'Discrétion'),
    ]
    cat_objs = {}
    for slug, nom in categories.items():
        obj, _ = CategorieTemplate.objects.get_or_create(slug=slug, defaults={'nom': nom})
        cat_objs[slug] = obj

    # --- 2. DONNÉES DE DÉMO (Contenu contextuel) ---
    DEMO_CONTENT = {
        'minimal_blanc': {
            'titre': 'Dr. Aminata Traoré',
            'bio': 'Médecin généraliste avec 15 ans d\'expérience. Consultations et médecine préventive à Bobo-Dioulasso.',
            'services': [
                ('Consultation générale', 'Examen complet adultes/enfants', '5 000 FCFA'),
                ('Suivi de grossesse', 'Accompagnement prénatal complet', '8 000 FCFA')
            ],
            'realisations': [
                ('Formation OMS', 'Urgences pédiatriques — Genève 2022'),
                ('Conférence UEMOA', 'Santé maternelle — Dakar 2023')
            ]
        },
        'bold_coral': {
            'titre': 'Menuiserie Kaboré & Fils',
            'bio': 'Spécialiste en meubles sur mesure et aménagements intérieurs depuis 2008. Qualité et tradition.',
            'services': [
                ('Meubles sur mesure', 'Tables et bibliothèques en bois noble', 'Dès 25 000 F'),
                ('Aménagement', 'Plafonds et parquets artisanaux', 'Sur devis')
            ],
            'realisations': [
                ('Villa Ouaga 2000', 'Aménagement d\'une villa 5 pièces'),
                ('Restaurant Le Cauri', 'Mobilier pour 80 couverts')
            ]
        },
        'tech_slate': {
            'titre': 'Ibrahim Coulibaly · Dev Mobile',
            'bio': 'Expert Flutter et React Native. 35+ applications livrées pour les startups d\'Afrique.',
            'services': [
                ('App iOS & Android', 'Développement natif et multiplateforme', 'Dès 250 000 F'),
                ('API Backend', 'Architecture robuste et paiement mobile', 'Dès 100 000 F')
            ],
            'realisations': [
                ('MaliPay App', '80 000 utilisateurs actifs au Mali'),
                ('AgriConnect', 'Marketplace pour 2 000 producteurs')
            ]
        },
        'prestige_events': {
            'titre': 'Sarah Traoré · Wedding Planner',
            'bio': 'Créatrice d\'événements d\'exception. Raffinement et élégance pour vos moments inoubliables.',
            'services': [
                ('Organisation Mariage', 'Coordination complète de votre grand jour', 'Dès 500 000 F'),
                ('Décoration de Gala', 'Scénographie florale haut de gamme', 'Sur devis')
            ],
            'realisations': [
                ('Mariage Royal', 'Réception de 500 invités au Palace'),
                ('Gala des Leaders', 'Décoration pour 200 chefs d\'entreprise')
            ]
        }
    }

    # --- 3. METADATA DES TEMPLATES (Design & Prix) ---
    templates_meta = [
        {
            'nom': 'Minimaliste Blanc', 'slug_t': 'minimal_blanc', 'cat': 'pro', 'premium': False,
            'colors': {'p': '#042C53', 'f': '#ffffff', 't': '#2C2C2A', 'a': '#185FA5'}
        },
        {
            'nom': 'Bold Coral', 'slug_t': 'bold_coral', 'cat': 'art', 'premium': True, 'price': 15000,
            'colors': {'p': '#D85A30', 'f': '#FAFAF8', 't': '#2C2C2A', 'a': '#993C1D'}
        },
        {
            'nom': 'Tech Slate', 'slug_t': 'tech_slate', 'cat': 'tech', 'premium': True, 'price': 25000,
            'colors': {'p': '#3B82F6', 'f': '#020617', 't': '#F8FAFC', 'a': '#60A5FA'}
        },
        {
            'nom': 'Prestige Events', 'slug_t': 'prestige_events', 'cat': 'event', 'premium': True, 'price': 35000,
            'colors': {'p': '#C9A84C', 'f': '#ffffff', 't': '#1A1A1A', 'a': '#A38637'}
        }
            ]
    for chiffre, label in stats_prestige:
        
            Statistique.objects.get_or_create(
                portfolio=portfolio_demo,
                chiffre=chiffre,
                label=label
            )
    self.stdout.write("✅ Stats de démo créées.")

    for t in templates_meta:
        TemplateMetadata.objects.update_or_create(
            slug=t['slug_t'].replace('_', '-'),
            defaults={
                'nom': t['nom'],
                'slug_technique': t['slug_t'],
                'categorie': cat_objs[t['cat']],
                'est_premium': t['premium'],
                'prix_cfa': t.get('price', 0),
                'couleur_primaire': t['colors']['p'],
                'couleur_accent': t['colors']['a'],
                'couleur_fond': t['colors']['f'],
                'couleur_texte': t['colors']['t'],
            }
        )
    print("✅ Métadonnées des templates synchronisées.")

    # --- 4. LE PORTFOLIO DE DÉMO (Source pour la galerie) ---
    demo_user, _ = User.objects.get_or_create(username="admin_demo")
    
    # On nettoie l'ancien demo-slug pour repartir sur du propre
    Portfolio.objects.filter(slug='demo-slug').delete()
    
    portfolio_demo = Portfolio.objects.create(
        user=demo_user,
        slug='demo-slug',
        titre="Expert WEBA Africa",
        bio="Ceci est un compte de démonstration pour illustrer les capacités de nos templates.",
        publie=True
    )

    # Ajout de services et réalisations génériques pour le demo-slug
    # (Ils seront écrasés visuellement par la logique DEMO_DATA dans tes vues)
    Service.objects.create(portfolio=portfolio_demo, titre="Service Démo", description="Description du service", prix="10 000 F")
    Realisation.objects.create(portfolio=portfolio_demo, titre="Projet Démo", description="Détails du projet")
    
    print("✅ Compte 'demo-slug' initialisé.")
    print("\n--- SEED TERMINÉ : WEBA est prêt pour la production ! ---")

if __name__ == '__main__':
    run_seed()