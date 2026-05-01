import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

# Imports locaux
from .models import Portfolio, POLICES, RAYONS
from .utils import get_contenu_demo

##############################################################################################################
##############################  PERSONNALISATION & DESIGN     ################################################
##############################################################################################################

@login_required
def customizer(request):
    """
    Interface d'édition en temps réel.
    - Portfolio vierge      → affiche couleurs d'usine + contenu démo
    - Portfolio personnalisé → affiche couleurs et contenu de l'utilisateur
    """
    portfolio = Portfolio.objects.filter(user=request.user).first()

    if not portfolio:
        return redirect('portfolio:template_list')

    template_nom = request.GET.get('template', portfolio.template_choisi)

    # Changement temporaire de template pour prévisualisation
    if template_nom != portfolio.template_choisi:
        portfolio.template_choisi = template_nom
        portfolio.est_personnalise = False 

    demo = get_contenu_demo(template_nom)

    if not portfolio.est_personnalise:
        portfolio.titre = demo.get('titre', portfolio.titre)
        portfolio.bio   = demo.get('bio', portfolio.bio)

    request.current_portfolio = portfolio

    return render(request, 'portfolio/customizer.html', {
        'portfolio':          portfolio,
        'polices':            POLICES,
        'rayons':             RAYONS,
        'template_a_afficher': template_nom,
        'tokens_fields': [
            ('couleur_primaire', 'Couleur principale'),
            ('couleur_accent',   "Couleur d'accent"),
            ('couleur_fond',     'Fond principal'),
            ('couleur_fond_2',   'Fond secondaire'),
            ('couleur_texte',    'Couleur du texte'),
        ],
    })

@login_required
@require_POST
def sauvegarder_tokens(request):
    """Sauvegarde les réglages CSS (couleurs, polices, arrondis) via JSON"""
    portfolio = get_object_or_404(Portfolio, user=request.user)
    try:
        data = json.loads(request.body)
        champs = [
            'couleur_primaire', 'couleur_accent', 'couleur_fond',
            'couleur_fond_2', 'couleur_texte', 'police', 'rayon_bordure'
        ]

        for champ in champs:
            if champ in data:
                setattr(portfolio, champ, data[champ])

        if 'template_choisi' in data:
            nouveau_template = data['template_choisi']
            if nouveau_template in [c[0] for c in Portfolio.CHOIX_TEMPLATES]:
                portfolio.template_choisi = nouveau_template

        portfolio.est_personnalise = True
        portfolio.save()

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def appliquer_palette(request, nom_palette):
    """Applique une combinaison de couleurs prédéfinie"""
    portfolio = get_object_or_404(Portfolio, user=request.user)

    palettes = {
        'coral':  {'couleur_primaire': '#D85A30', 'couleur_accent': '#993C1D', 'couleur_fond': '#FAFAF8', 'couleur_fond_2': '#FAECE7', 'couleur_texte': '#2C2C2A'},
        'ocean':  {'couleur_primaire': '#2563EB', 'couleur_accent': '#1E40AF', 'couleur_fond': '#F8FAFC', 'couleur_fond_2': '#EFF6FF', 'couleur_texte': '#1E293B'},
        'forest': {'couleur_primaire': '#1D9E75', 'couleur_accent': '#0F6E56', 'couleur_fond': '#F0FDF4', 'couleur_fond_2': '#DCFCE7', 'couleur_texte': '#14532D'},
        'onyx':   {'couleur_primaire': '#C9A84C', 'couleur_accent': '#EF9F27', 'couleur_fond': '#0A0A0A', 'couleur_fond_2': '#111111', 'couleur_texte': '#F5F5F5'},
        'violet': {'couleur_primaire': '#7F77DD', 'couleur_accent': '#5DCAA5', 'couleur_fond': '#26215C', 'couleur_fond_2': '#3C3489', 'couleur_texte': '#EEEDFE'},
        'terre':  {'couleur_primaire': '#D4874E', 'couleur_accent': '#2D1B0E', 'couleur_fond': '#FDF8F3', 'couleur_fond_2': '#FAF0E6', 'couleur_texte': '#2D1B0E'},
    }

    palette = palettes.get(nom_palette)
    if palette:
        for champ, valeur in palette.items():
            setattr(portfolio, champ, valeur)
        portfolio.save()

    return JsonResponse({'status': 'ok', 'palette': palette})

@login_required
def changer_template(request):
    """Change le modèle via HTMX (utilisé dans le dashboard ou customizer)"""
    portfolio_inst = get_object_or_404(Portfolio, user=request.user)

    if request.method == 'POST':
        nouveau_template = request.POST.get('template_choisi')
        templates_valides = [choice[0] for choice in Portfolio.CHOIX_TEMPLATES]
        
        if nouveau_template in templates_valides:
            portfolio_inst.template_choisi = nouveau_template
            portfolio_inst.save()

            return render(request, 'portfolio/partials/succes_template.html', {
                'template_nom': portfolio_inst.get_template_choisi_display()
            })
        
        return HttpResponse("<span class='text-red-500'>Modèle invalide.</span>", status=400)

    return HttpResponse(status=405)

@login_required
def appliquer_et_customiser(request, template_slug):
    """Initialise le template et redirige vers l'interface d'édition"""
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user,
        defaults={
            'slug':  slugify(request.user.username),
            'titre': f"Portfolio de {request.user.username}",
        }
    )

    portfolio.template_choisi  = template_slug
    portfolio.est_personnalise = False
    portfolio.couleur_primaire = None
    portfolio.couleur_accent   = None
    portfolio.couleur_fond     = None
    portfolio.couleur_fond_2   = None
    portfolio.couleur_texte    = None
    portfolio.save()

    return redirect('portfolio:customizer')

@login_required
def modifier_portfolio(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    
    if request.method == 'POST':
        nouveau_theme = request.POST.get('template_choisi')
        if nouveau_theme:
            THEMES_PRO = ['tech_slate', 'bold_coral']
            if nouveau_theme in THEMES_PRO:
                if not hasattr(request.user, 'abonnement') or request.user.abonnement.plan.nom not in ['pro', 'business']:
                    nouveau_theme = 'minimal'

            portfolio.template_choisi = nouveau_theme
            portfolio.save(update_fields=['template_choisi'])
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)