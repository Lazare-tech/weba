from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from core.email_utils import envoyer_email_html


@shared_task(name='envoyer_email_bienvenue')
def envoyer_email_bienvenue(user_id, nom_blog):
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(id=user_id)
        envoyer_email_html(
            sujet='Bienvenue sur WEBA !',
            template='emails/bienvenue.html',
            context={
                'username': user.username,
                'nom_blog': nom_blog,
                'blog_url': f'http://localhost:8000/pages/{user.profil.blog.slug}/',
            },
            destinataire=user.email,
        )
        return f"Email envoyé à {user.email}"
    except Exception as e:
        return f"Erreur: {e}"


@shared_task(name='notifier_nouveau_commentaire')
def notifier_nouveau_commentaire(commentaire_id):
    from blog.models import Commentaire
    try:
        commentaire = Commentaire.objects.get(id=commentaire_id)
        blog = commentaire.page.get_parent().specific
        proprietaire = blog.proprietaire.user

        envoyer_email_html(
            sujet=f'Nouveau commentaire sur "{commentaire.page.title}"',
            template='emails/nouveau_commentaire.html',
            context={
                'username': proprietaire.username,
                'auteur': commentaire.auteur,
                'titre_article': commentaire.page.title,
                'contenu': commentaire.contenu,
                'dashboard_url': 'http://localhost:8000/dashboard/',
            },
            destinataire=proprietaire.email,
        )
        return f"Notification envoyée à {proprietaire.email}"
    except Exception as e:
        return f"Erreur: {e}"


@shared_task(name='notifier_nouveau_message_portfolio')
def notifier_nouveau_message_portfolio(message_id):
    from portfolio.models import MessageContact
    try:
        msg = MessageContact.objects.get(id=message_id)
        proprietaire = msg.portfolio.user

        envoyer_email_html(
            sujet=f'Nouveau message de {msg.nom} via votre portfolio',
            template='emails/nouveau_message_portfolio.html',
            context={
                'username': proprietaire.username,
                'nom': msg.nom,
                'email': msg.email,
                'telephone': msg.telephone,
                'message': msg.message,
            },
            destinataire=proprietaire.email,
        )
        return f"Notification envoyée à {proprietaire.email}"
    except Exception as e:
        return f"Erreur: {e}"


@shared_task(name='rappel_abonnement_expirant')
def rappel_abonnement_expirant():
    from abonnements.models import Abonnement
    from django.utils import timezone
    from datetime import timedelta

    dans_3_jours = timezone.now() + timedelta(days=3)
    abonnements = Abonnement.objects.filter(
        actif=True,
        date_fin__date=dans_3_jours.date()
    ).select_related('user', 'plan')

    for abonnement in abonnements:
        envoyer_email_html(
            sujet='Votre abonnement WEBA expire dans 3 jours',
            template='emails/rappel_abonnement.html',
            context={
                'username': abonnement.user.username,
                'plan': abonnement.plan,
                'date_fin': abonnement.date_fin.strftime('%d/%m/%Y'),
                'tarification_url': 'http://localhost:8000/tarification/',
            },
            destinataire=abonnement.user.email,
        )

    return f"{abonnements.count()} rappel(s) envoyé(s)"


@shared_task(name='nettoyer_sessions')
def nettoyer_sessions():
    from django.contrib.sessions.backends.db import SessionStore
    SessionStore.clear_expired()
    return "Sessions nettoyées"

@shared_task(name='generer_sitemap')
def generer_sitemap():
    """Régénère le cache du sitemap"""
    from django.test import RequestFactory
    from django.contrib.sitemaps.views import sitemap
    from seo.sitemaps import BlogIndexSitemap, BlogPostSitemap

    sitemaps = {
        'blogs': BlogIndexSitemap,
        'articles': BlogPostSitemap,
    }

    factory = RequestFactory()
    request = factory.get('/sitemap.xml')
    sitemap(request, sitemaps=sitemaps)

    return "Sitemap régénéré"


@shared_task(name='nettoyer_sessions')
def nettoyer_sessions():
    """Supprime les sessions Django expirées"""
    from django.contrib.sessions.backends.db import SessionStore
    SessionStore.clear_expired()
    return "Sessions nettoyées"