from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan, Abonnement, DemandeUpgrade


def tarification(request):
    """Page publique de tarification"""
    plans = Plan.objects.all().order_by('prix_mensuel')
    plan_actuel = None

    if request.user.is_authenticated:
        try:
            plan_actuel = request.user.abonnement.plan.nom
        except Exception:
            plan_actuel = 'gratuit'

    return render(request, 'abonnements/tarification.html', {
        'plans': plans,
        'plan_actuel': plan_actuel,
    })


@login_required
def demander_upgrade(request, nom_plan):
    """L'utilisateur soumet une demande d'upgrade avec référence de paiement"""
    plan = Plan.objects.get(nom=nom_plan)

    if request.method == 'POST':
        reference = request.POST.get('reference_paiement', '').strip()
        message = request.POST.get('message', '').strip()

        if not reference:
            messages.error(request, "La référence de paiement est obligatoire.")
            return render(request, 'abonnements/demande_upgrade.html', {
                'plan': plan
            })

        DemandeUpgrade.objects.create(
            user=request.user,
            plan_demande=plan,
            reference_paiement=reference,
            message=message,
        )

        messages.success(
            request,
            "Demande envoyée ! Votre plan sera activé après vérification du paiement."
        )
        return redirect('dashboard')

    return render(request, 'abonnements/demande_upgrade.html', {'plan': plan})


@login_required
def activer_plan(request, user_id, nom_plan):
    """Admin seulement — active le plan d'un utilisateur"""
    if not request.user.is_superuser:
        return redirect('dashboard')

    from django.contrib.auth.models import User
    from django.utils import timezone
    from datetime import timedelta

    user = User.objects.get(id=user_id)
    plan = Plan.objects.get(nom=nom_plan)

    # Crée ou met à jour l'abonnement
    abonnement, _ = Abonnement.objects.update_or_create(
        user=user,
        defaults={
            'plan': plan,
            'actif': True,
            'date_fin': timezone.now() + timedelta(days=30),
        }
    )

    # Met à jour le profil
    user.profil.plan = nom_plan
    user.profil.save()

    # Approuve la demande en attente
    DemandeUpgrade.objects.filter(
        user=user, statut='en_attente'
    ).update(statut='approuve')

    messages.success(request, f"Plan {plan} activé pour {user.username} !")
    return redirect('admin_demandes')


@login_required
def admin_demandes(request):
    """Vue admin pour gérer les demandes d'upgrade"""
    if not request.user.is_superuser:
        return redirect('dashboard')

    demandes = DemandeUpgrade.objects.filter(
        statut='en_attente'
    ).select_related('user', 'plan_demande')

    return render(request, 'abonnements/admin_demandes.html', {
        'demandes': demandes
    })
#############################################
from abonnements.decorators import require_plan

@login_required
@require_plan('pro', 'business')
def analytics(request):
    # Seulement accessible aux plans Pro et Business
    ...

@login_required
@require_plan('business')
def app_web(request):
    # Seulement accessible au plan Business
    ...