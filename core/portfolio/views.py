import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.cache import never_cache

# Imports locaux
from .models import Portfolio, TemplateMetadata, POLICES, RAYONS
from .utils import get_contenu_demo, get_tokens_pour_template
# (Garde ces imports si tu comptes ajouter les fonctions CRUD ci-dessous)
# from .forms import PortfolioForm, RealisationForm, ServiceForm, StatistiqueForm, TemoignageForm, MessageContactForm

## GESTION DU PORTFOLIO

@never_cache
@xframe_options_sameorigin
def portfolio_public(request, slug):
    """
    Affiche le vrai portfolio de l'utilisateur.
    """
    portfolio = get_object_or_404(Portfolio, slug=slug)
    request.current_portfolio = portfolio

    theme_id = portfolio.template_choisi
    demo     = get_contenu_demo(theme_id)

    if portfolio.est_personnalise:
        services     = portfolio.services.all()
        realisations = portfolio.realisations.all()
        temoignages  = portfolio.temoignages.filter(approuve=True)
        is_demo      = False
    else:
        portfolio.titre = demo.get('titre', portfolio.titre)
        portfolio.bio   = demo.get('bio', portfolio.bio)

        class ServiceDemo:
            def __init__(self, d):
                if isinstance(d, dict):
                    self.titre, self.description, self.prix = d.get('titre',''), d.get('description',''), d.get('prix','')
                    self.image = type('FakeImage', (), {'url': '/static/images/demo-service.jpg'})()
                else:
                    self.titre, self.description, self.prix = d[0], d[1], d[2] if len(d) > 2 else ''

        class RealisationDemo:
            def __init__(self, d):
                if isinstance(d, dict):
                    self.titre, self.description = d.get('titre',''), d.get('description','')
                else:
                    self.titre, self.description = d[0], d[1]
                self.image, self.lien, self.date = None, '', None

        services     = [ServiceDemo(s)     for s in demo.get('services', [])]
        realisations = [RealisationDemo(r) for r in demo.get('realisations', [])]
        temoignages  = []
        is_demo      = True

    theme_template = f'portfolio/themes/{theme_id}/public.html'
    try:
        get_template(theme_template)
    except TemplateDoesNotExist:
        theme_template = 'portfolio/themes/minimal_blanc/public.html'

    return render(request, theme_template, {
        'portfolio':    portfolio,
        'realisations': realisations,
        'services':     services,
        'temoignages':  temoignages,
        'is_demo':      is_demo,
    })

def creer_portfolio(request):
    if hasattr(request.user, 'portfolio'):
        return redirect('portfolio:dashboard_portfolio')

    if request.method == 'POST':
        template_slug = request.POST.get('template_choisi', 'minimal')
        slug_base = slugify(request.user.username)
        slug = slug_base
        compteur = 1
        while Portfolio.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{compteur}"
            compteur += 1
            
        Portfolio.objects.create(
            user=request.user,
            slug=slug,
            template_choisi=template_slug,
            titre=f"Portfolio de {request.user.username}",
            bio="[Cliquez ici pour décrire votre activité et votre expertise]",
            publie=True
        )
        
        messages.success(request, "Félicitations ! Votre site est prêt.")
        return redirect('portfolio:dashboard_portfolio')

    return render(request, 'portfolio/choisir_template.html')

@login_required
def dashboard_portfolio(request):
    portfolio_inst = Portfolio.objects.filter(user=request.user).first()
    context = {'portfolio': portfolio_inst}

    if portfolio_inst:
        context.update({
            'realisations': portfolio_inst.realisations.all(),
            'services': portfolio_inst.services.all(),
            'temoignages': portfolio_inst.temoignages.all(),
            'messages_recus': portfolio_inst.messages.filter(lu=False).count(),
        })
    return render(request, 'portfolio/dashboard.html', context)

@login_required
def modifier_infos(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)

    if request.GET.get('cancel'):
        return render(request, 'portfolio/partials/identite_content.html', {'portfolio': portfolio})

    if request.method == 'POST':
        portfolio.titre         = request.POST.get('titre', portfolio.titre)
        portfolio.bio           = request.POST.get('bio', portfolio.bio)
        portfolio.telephone     = request.POST.get('telephone', portfolio.telephone)
        portfolio.email_contact = request.POST.get('email_contact', portfolio.email_contact)
        
        nouvelle_photo = request.FILES.get('photo')
        if nouvelle_photo:
            portfolio.photo = nouvelle_photo
            
        portfolio.save()
        return render(request, 'portfolio/partials/identite/identite_content.html', {'portfolio': portfolio})

    return render(request, 'portfolio/partials/identite/form_identite.html', {'portfolio': portfolio})

def portfolio_detail(request):
    return render(request, 'portfolio/portfolio_detail_temp.html')


def portfolio_public_view(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug, publie=True)
    return render(request, f"portfolio/{portfolio.template_choisi}.html", {
        'portfolio': portfolio,
        'realisations': portfolio.realisations.all(),
        'services': portfolio.services.all(),
        'temoignages': portfolio.temoignages.filter(approuve=True),
    })