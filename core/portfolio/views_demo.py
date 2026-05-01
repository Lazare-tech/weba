from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.cache import never_cache

# Imports locaux
from .models import CategorieTemplate, TemplateMetadata
from .utils import get_tokens_pour_template, get_contenu_demo

##############################################################################################################
##############################       GALERIE ET APERCU         ###############################################
##############################################################################################################

def template_list(request):
    """Catalogue de tous les thèmes disponibles avec filtrage par catégorie"""
    categorie_slug = request.GET.get('categorie')
    templates = TemplateMetadata.objects.all()
    
    if categorie_slug:
        templates = templates.filter(categorie__slug=categorie_slug)

    # Support HTMX : renvoie uniquement la grille si la requête provient d'HTMX
    if request.headers.get('HX-Request'):
        return render(request, 'portfolio/partials/template_grid.html', {'templates': templates})

    categories = CategorieTemplate.objects.all()
    return render(request, 'portfolio/template_list.html', {
        'templates': templates,
        'categories': categories
    })

def template_detail(request, slug):
    """Présentation détaillée d'un thème spécifique et suggestions"""
    template = get_object_or_404(TemplateMetadata, slug=slug)
    suggestions = TemplateMetadata.objects.filter(categorie=template.categorie).exclude(id=template.id)[:3]
    
    return render(request, 'portfolio/template_detail.html', {
        'template': template,
        'suggestions': suggestions
    })

@xframe_options_sameorigin
def portfolio_demo(request, slug):
    """Page conteneur de la démo (Frame de l'appareil + Iframe de contenu)"""
    template_meta = get_object_or_404(TemplateMetadata, slug=slug)
    tokens = get_tokens_pour_template(template_meta.slug_technique)

    return render(request, 'portfolio/partials/portfolio_demo.html', {
        'template':      template_meta,
        'design_tokens': tokens,
    })

@never_cache
@xframe_options_sameorigin
def portfolio_demo_apercu(request, slug):
    """
    Iframe sandbox : Affiche le template avec données fictives (DEMO_DATA)
    et couleurs d'usine, sans dépendance au portfolio réel de l'utilisateur.
    """
    template_meta = get_object_or_404(TemplateMetadata, slug=slug)
    slug_technique = template_meta.slug_technique

    # Récupération des réglages et contenus de démo
    tokens = get_tokens_pour_template(slug_technique)
    demo = get_contenu_demo(slug_technique)

    # Polymorphisme : On crée un objet fictif qui imite le modèle Portfolio
    class PortfolioApercu:
        titre            = demo.get('titre', template_meta.nom)
        bio              = demo.get('bio', "Présentation de démonstration.")
        secteur          = demo.get('secteur', 'Expertise')
        ville            = demo.get('ville', 'Ouagadougou')
        telephone        = demo.get('telephone', '+226 00 00 00 00')
        email_contact    = demo.get('email', 'contact@weba.bf')
        slug             = f'apercu-{slug_technique}'
        est_personnalise = False
        template_choisi  = slug_technique
        publie           = True
        photo            = None
        whatsapp = facebook = linkedin = instagram = ''

        # Injection des tokens de design
        couleur_primaire = tokens['couleur_primaire']
        couleur_accent   = tokens['couleur_accent']
        couleur_fond     = tokens['couleur_fond']
        couleur_fond_2   = tokens['couleur_fond_2']
        couleur_texte    = tokens['couleur_texte']
        rayon_bordure    = tokens['rayon_bordure']
        police           = 'inter'

        user = type('FakeUser', (), {
            'username': demo.get('titre', 'Demo').split('·')[0].strip()
        })()

        def get_police_family(self): return tokens['police_family']
        def get_police_url(self): return tokens['police_url']
        def get_absolute_url(self): return '#'

    # Simulation des listes de contenu
    class ServiceApercu:
        def __init__(self, d):
            self.titre = d.get('titre', '') if isinstance(d, dict) else d[0]
            self.description = d.get('description', '') if isinstance(d, dict) else d[1]
            self.prix = d.get('prix', '') if isinstance(d, dict) else (d[2] if len(d) > 2 else '')
            self.image = type('Img', (), {'url': '/static/images/demo/service.jpg'})()

    class RealisationApercu:
        def __init__(self, d):
            self.titre = d.get('titre', '') if isinstance(d, dict) else d[0]
            self.description = d.get('description', '') if isinstance(d, dict) else d[1]
            self.image = None
            self.lien = ''

    class TemoignageApercu:
        def __init__(self, d):
            self.nom_client = d.get('nom_client', '')
            self.entreprise = d.get('entreprise', 'Partenaire')
            self.contenu = d.get('contenu', '')
            self.note = d.get('note', 5)

    services     = [ServiceApercu(s)     for s in demo.get('services', [])]
    realisations = [RealisationApercu(r) for r in demo.get('realisations', [])]
    temoignages  = [TemoignageApercu(t)  for t in demo.get('temoignages', [])]

    portfolio_apercu = PortfolioApercu()
    request.current_portfolio = portfolio_apercu

    # Sélection du template ou fallback sur le template minimal
    theme_template = f'portfolio/themes/{slug_technique}/public.html'
    try:
        get_template(theme_template)
    except TemplateDoesNotExist:
        theme_template = 'portfolio/themes/minimal_blanc/public.html'

    return render(request, theme_template, {
        'portfolio':    portfolio_apercu,
        'realisations': realisations,
        'services':     services,
        'temoignages':  temoignages,
        'design_tokens': tokens,
        'is_demo':      True,
    })