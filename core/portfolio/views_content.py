from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.core.mail import send_mail
from django.conf import settings

# Imports locaux
from .models import Portfolio, Realisation, Service, Statistique, Temoignage, MessageContact
from .forms import RealisationForm, ServiceForm, StatistiqueForm, TemoignageForm

##############################################################################################################
##############################  GESTION DU CONTENU (CRUD)    ################################################
##############################################################################################################

# --- RÉALISATIONS ---
@login_required
def ajouter_realisation(request):
    portfolio_inst = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES)
        if form.is_valid():
            realisation = form.save(commit=False)
            realisation.portfolio = portfolio_inst
            realisation.save()
            return render(request, 'portfolio/partials/realisation_item.html', {'r': realisation})
    else:
        form = RealisationForm()
    return render(request, 'portfolio/partials/form_realisation.html', {'form': form})

@login_required
def modifier_realisation(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk, portfolio__user=request.user)
    if request.GET.get('cancel'):
        return render(request, 'portfolio/partials/realisations/realisation_item.html', {'r': realisation})

    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES, instance=realisation)
        if form.is_valid():
            realisation = form.save()
            return render(request, 'portfolio/partials/realisations/realisation_item.html', {'r': realisation})
    else:
        form = RealisationForm(instance=realisation)
    return render(request, 'portfolio/partials/realisations/form_realisation.html', {'form': form, 'realisation': realisation})

@login_required
@require_http_methods(["DELETE", "POST"])
def supprimer_realisation(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk, portfolio__user=request.user)
    realisation.delete()
    return HttpResponse('')

# --- SERVICES ---
@login_required
def ajouter_service(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES) 
        if form.is_valid():
            service = form.save(commit=False)
            service.portfolio = portfolio
            service.save()
            return render(request, 'portfolio/partials/services/service_item.html', {'s': service})
    else:
        form = ServiceForm()
    return render(request, 'portfolio/partials/services/form_service.html', {'form': form})

@login_required
def modifier_service(request, pk):
    service = get_object_or_404(Service, pk=pk, portfolio__user=request.user)
    if request.GET.get('cancel'):
        return render(request, 'portfolio/partials/services/service_item.html', {'s': service})

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save()
            return render(request, 'portfolio/partials/services/service_item.html', {'s': service})
    else:
        form = ServiceForm(instance=service)
    return render(request, 'portfolio/partials/services/form_service.html', {'form': form, 'service': service})

@login_required
@require_http_methods(["DELETE", "POST"])
def supprimer_service(request, pk):
    service = get_object_or_404(Service, pk=pk, portfolio__user=request.user)
    service.delete()
    return HttpResponse("")

# --- STATISTIQUES ---
@login_required
def ajouter_stat(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = StatistiqueForm(request.POST)
        if form.is_valid():
            stat = form.save(commit=False)
            stat.portfolio = portfolio
            stat.save()
            return render(request, 'portfolio/partials/stat_item.html', {'stat': stat})
    else:
        form = StatistiqueForm()
    return render(request, 'portfolio/partials/form_stat.html', {'form': form})

@login_required
def gerer_statistique(request, pk=None):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    stat = get_object_or_404(Statistique, pk=pk, portfolio=portfolio) if pk else None
    if request.method == 'POST':
        form = StatistiqueForm(request.POST, instance=stat)
        if form.is_valid():
            new_stat = form.save(commit=False)
            new_stat.portfolio = portfolio
            new_stat.save()
            return render(request, 'portfolio/partials/stat_item.html', {'stat': new_stat})
    form = StatistiqueForm(instance=stat)
    return render(request, 'portfolio/partials/form_stat.html', {'form': form, 'stat': stat})

@login_required
@require_POST
def supprimer_stat(request, pk):
    stat = get_object_or_404(Statistique, pk=pk, portfolio__user=request.user)
    stat.delete()
    return HttpResponse("")

##############################################################################################################
##############################  INTERACTIONS (AVIS & MESSAGES) ################################################
##############################################################################################################

# --- TÉMOIGNAGES ---
@require_POST
def laisser_avis_public(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug)
    nom = request.POST.get('nom_client')
    entreprise = request.POST.get('entreprise')
    contenu = request.POST.get('contenu')
    note = request.POST.get('note', 5)

    if nom and contenu:
        Temoignage.objects.create(portfolio=portfolio, nom_client=nom, entreprise=entreprise, contenu=contenu, note=int(note), approuve=False)
        return HttpResponse('<div class="text-center py-12"><h3>Merci ! Votre avis est en cours de validation.</h3></div>')
    return HttpResponse("Erreur dans le formulaire", status=400)

@login_required
def approuver_temoignage(request, pk):
    temoignage = get_object_or_404(Temoignage, pk=pk, portfolio__user=request.user)
    temoignage.approuve = not temoignage.approuve
    temoignage.save()
    return render(request, 'portfolio/partials/temoignage_item.html', {'t': temoignage})

@login_required
@require_http_methods(["DELETE", "POST"])
def supprimer_temoignage(request, pk):
    get_object_or_404(Temoignage, pk=pk, portfolio__user=request.user).delete()
    return HttpResponse("")

# --- MESSAGES DE CONTACT ---
@require_POST
def envoyer_message(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug)
    msg = MessageContact.objects.create(
        portfolio=portfolio,
        nom=request.POST.get('nom'),
        email=request.POST.get('email'),
        sujet=request.POST.get('sujet', 'Nouveau contact'),
        telephone=request.POST.get('telephone'),
        message=request.POST.get('message')
    )
    # Email notification
    try:
        send_mail(f"Nouveau message : {msg.nom}", msg.message, settings.DEFAULT_FROM_EMAIL, [portfolio.user.email], fail_silently=True)
    except: pass
    return HttpResponse('<div class="text-emerald-600 font-bold">Message envoyé avec succès !</div>')

@login_required
def messages_recus(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    msgs = portfolio.messages.all().order_by('-date')
    return render(request, 'portfolio/partials/message/messages_recus.html', {'portfolio': portfolio, 'messages': msgs})

@login_required
def marquer_lu_message(request, pk):
    msg = get_object_or_404(MessageContact, pk=pk, portfolio__user=request.user)
    msg.lu = True
    msg.save()
    return render(request, 'portfolio/partials/message_item.html', {'m': msg})

@login_required
@require_http_methods(["DELETE", "POST"])
def supprimer_message(request, pk):
    get_object_or_404(MessageContact, pk=pk, portfolio__user=request.user).delete()
    return HttpResponse("")

# --- RÉSEAUX SOCIAUX ---
@login_required
def modifier_reseaux(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        portfolio.whatsapp = request.POST.get('whatsapp')
        portfolio.facebook = request.POST.get('facebook')
        portfolio.linkedin = request.POST.get('linkedin')
        portfolio.instagram = request.POST.get('instagram')
        portfolio.save()
        return render(request, 'portfolio/partials/reseaux_content.html', {'portfolio': portfolio})
    
    if request.GET.get('cancel'):
         return render(request, 'portfolio/partials/reseaux_content.html', {'portfolio': portfolio})
    return render(request, 'portfolio/partials/form_reseaux.html', {'portfolio': portfolio})