from django.shortcuts import render
from .models import Entreprise
# Create your views here.


def index(request):
    return render(request, 'search/index.html')

def recherche(request):
    query = request.GET.get('q', '')
    resultats = Entreprise.objects.filter(
        nom__icontains=query
    ) if query else Entreprise.objects.all()
    
    # HTMX attend un fragment HTML, pas une page complète
    return render(request, 'search/partials/resultats.html', {
        'resultats': resultats,
        'query': query
    })
###
from django.http import HttpResponse
from .forms import EntrepriseForm

def ajouter(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            # On renvoie le formulaire vide + message succès
            return render(request, 'search/partials/formulaire.html', {
                'form': EntrepriseForm(),
                'succes': True
            })
        # Formulaire invalide : on renvoie avec erreurs
        return render(request, 'search/partials/formulaire.html', {
            'form': form,
            'succes': False
        })

    # GET : affiche le formulaire vide
    return render(request, 'search/partials/formulaire.html', {
        'form': EntrepriseForm()
    })

def liste_complete(request):
    entreprises = Entreprise.objects.all().order_by('-id')
    return render(request, 'search/partials/resultats.html', {
        'resultats': entreprises
    })
##
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def supprimer(request, pk):
    if request.method == 'DELETE':
        Entreprise.objects.filter(pk=pk).delete()
        # On renvoie la liste mise à jour
        entreprises = Entreprise.objects.all().order_by('-id')
        return render(request, 'search/partials/resultats.html', {
            'resultats': entreprises
        })