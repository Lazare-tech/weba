from .models import TemplateMetadata
from .constants import DEMO_DATA


def get_tokens_pour_template(slug_technique):
    """
    Retourne les tokens de design d'usine d'un template.
    Source : TemplateMetadata en base de données.
    """
    meta = TemplateMetadata.objects.filter(
        slug_technique=slug_technique
    ).first()

    if not meta:
        return {
            'couleur_primaire': '#10b981',
            'couleur_accent':   '#059669',
            'couleur_fond':     '#ffffff',
            'couleur_fond_2':   '#f8fafc',
            'couleur_texte':    '#0f172a',
            'police_family':    "'Inter', sans-serif",
            'police_url':       None,
            'rayon_bordure':    '0.75rem',
        }

    return {
        'couleur_primaire': meta.couleur_primaire,
        'couleur_accent':   meta.couleur_accent,
        'couleur_fond':     meta.couleur_fond,
        'couleur_fond_2':   meta.couleur_fond_2,
        'couleur_texte':    meta.couleur_texte,
        'police_family':    meta.police_nom or "'Inter', sans-serif",
        'police_url':       meta.police_url,
        'rayon_bordure':    meta.rayon_bordure,
    }


def get_contenu_demo(slug_technique):
    """
    Retourne le contenu fictif d'un template.
    Source : DEMO_DATA dans constants.py.
    """
    return DEMO_DATA.get(slug_technique, {})


def construire_context_portfolio(portfolio):
    """
    Construit le dictionnaire design_tokens selon l'état du portfolio.
    - Pas personnalisé → tokens d'usine depuis TemplateMetadata
    - Personnalisé      → tokens sauvegardés dans Portfolio
    """
    if portfolio.est_personnalise:
        return {
            'couleur_primaire': portfolio.couleur_primaire,
            'couleur_accent':   portfolio.couleur_accent,
            'couleur_fond':     portfolio.couleur_fond,
            'couleur_fond_2':   portfolio.couleur_fond_2,
            'couleur_texte':    portfolio.couleur_texte,
            'police_family':    portfolio.get_police_family(),
            'police_url':       portfolio.get_police_url(),
            'rayon_bordure':    portfolio.rayon_bordure,
        }
    else:
        return get_tokens_pour_template(portfolio.template_choisi)