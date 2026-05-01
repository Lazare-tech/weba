from django.core.management.base import BaseCommand
from abonnements.models import Plan


class Command(BaseCommand):
    help = 'Initialise les plans WEBA'

    def handle(self, *args, **kwargs):
        plans = [
            {
                'nom': 'gratuit',
                'prix_mensuel': 0,
                'description': 'Démarrez gratuitement avec un blog complet',
                'templates_premium': False,
                'analytics_avances': False,
                'portfolio': False,
                'ia_branding': False,
                'app_web': False,
                'automatisations': False,
                'portfolio_equipe': False,
            },
            {
                'nom': 'pro',
                'prix_mensuel': 5000,
                'description': 'Pour les professionnels qui veulent plus de visibilité',
                'templates_premium': True,
                'analytics_avances': True,
                'portfolio': True,
                'ia_branding': True,
                'app_web': False,
                'automatisations': False,
                'portfolio_equipe': False,
            },
            {
                'nom': 'business',
                'prix_mensuel': 15000,
                'description': 'La solution complète pour les entreprises',
                'templates_premium': True,
                'analytics_avances': True,
                'portfolio': True,
                'ia_branding': True,
                'app_web': True,
                'automatisations': True,
                'portfolio_equipe': True,
            },
        ]

        for data in plans:
            plan, created = Plan.objects.update_or_create(
                nom=data['nom'],
                defaults=data
            )
            status = 'créé' if created else 'mis à jour'
            self.stdout.write(f"Plan {plan} {status} ✅")