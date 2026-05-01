from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def envoyer_email_html(sujet, template, context, destinataire):
    """Envoie un email HTML avec fallback texte"""
    html_content = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject=sujet,
        body=f"Bonjour,\n\nVeuillez consulter cet email dans un client supportant le HTML.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinataire],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)