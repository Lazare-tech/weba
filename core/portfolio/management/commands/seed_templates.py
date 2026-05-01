from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    TemplateMetadata, CategorieTemplate, Portfolio, 
    Service, Realisation, Statistique
)

class Command(BaseCommand):
    help = 'Peuple ou met à jour la base de données sans destruction'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Synchronisation du Seed WEBA Africa..."))

        # --- 1. CATÉGORIES (Idempotent) ---
        categories_data = {
            'pro': 'Professionnel',
            'art': 'Artisanat & BTP',
            'tech': 'Technologie',
            'event': 'Événementiel'
        }
        cat_objs = {}
        for slug, nom in categories_data.items():
            obj, _ = CategorieTemplate.objects.get_or_create(slug=slug, defaults={'nom': nom})
            cat_objs[slug] = obj

        # --- 2. TEMPLATES (Mise à jour automatique des couleurs/prix) ---
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
                'nom': 'Creative Can', 'slug_t': 'creative_can', 'cat': 'tech', 'premium': True, 'price': 30000,
                'colors': {'p': '#7C3AED', 'f': '#0F172A', 't': '#F8FAFC', 'a': '#EC4899'}
            },
            {
                'nom': 'Prestige Events', 'slug_t': 'prestige_events', 'cat': 'event', 'premium': True, 'price': 35000,
                'colors': {'p': '#C9A84C', 'f': '#ffffff', 't': '#1A1A1A', 'a': '#A38637'}
            }
        ]

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

        # --- 3. PORTFOLIO DE DÉMO (Mise à jour sans suppression) ---
        demo_user, _ = User.objects.get_or_create(username="admin_demo")
        
        # On utilise update_or_create au lieu de delete() + create()
        portfolio_demo, created = Portfolio.objects.update_or_create(
            slug='demo-slug',
            defaults={
                'user': demo_user,
                'titre': "Expert WEBA Africa",
                'bio': "Compte de démonstration illustrant les capacités de nos thèmes.",
                'publie': True,
                'template_choisi': 'minimal-blanc' # Template par défaut
            }
        )

        # --- 4. STATISTIQUES (Eviter les doublons par label) ---
        stats_data = [
            ('150', 'Mariages'),
            ('08', 'Pays explorés'),
            ('24k', 'Fleurs dressées'),
            ('100%', 'Discrétion'),
        ]
        
        for chiffre, label in stats_data:
            Statistique.objects.update_or_create(
                portfolio=portfolio_demo,
                label=label,
                defaults={'chiffre': chiffre}
            )

        # --- 5. SERVICES & RÉALISATIONS (Mise à jour par titre) ---
        Service.objects.update_or_create(
            portfolio=portfolio_demo,
            titre="Service Démo",
            defaults={
                'description': "Exemple de prestation proposée.",
                'prix': "10 000 F"
            }
        )

        Realisation.objects.update_or_create(
            portfolio=portfolio_demo,
            titre="Projet Démo",
            defaults={
                'description': "Exemple de projet réalisé avec succès."
            }
        )
        
        self.stdout.write(self.style.SUCCESS("✅ Synchronisation terminée avec succès !"))