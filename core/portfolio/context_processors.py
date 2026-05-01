from .utils import construire_context_portfolio, get_tokens_pour_template


def portfolio_tokens(request):
    """
    Injecte les design_tokens dans tous les templates.
    Supporte les vrais Portfolio, les objets démo et les previews.
    """
    # Cas 1 — tokens injectés directement (démo template_list)
    tokens_directs = getattr(request, 'design_tokens_directs', None)
    if tokens_directs:
        return {'design_tokens': tokens_directs}

    # Cas 2 — portfolio stocké dans request (portfolio_public, customizer)
    portfolio = getattr(request, 'current_portfolio', None)
    if not portfolio:
        return {}

    # Si c'est un objet fictif (PortfolioDemo) → il a déjà ses tokens
    if hasattr(portfolio, '_est_demo') and portfolio._est_demo:
        return {
            'design_tokens': {
                'couleur_primaire': portfolio.couleur_primaire,
                'couleur_accent':   portfolio.couleur_accent,
                'couleur_fond':     portfolio.couleur_fond,
                'couleur_fond_2':   portfolio.couleur_fond_2,
                'couleur_texte':    portfolio.couleur_texte,
                'police_family':    portfolio.get_police_family(),
                'police_url':       portfolio.get_police_url(),
                'rayon_bordure':    portfolio.rayon_bordure,
            }
        }

    # Cas 3 — vrai portfolio → selon est_personnalise
    return {'design_tokens': construire_context_portfolio(portfolio)}