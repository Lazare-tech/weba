from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm, ProfilForm
from .models import creer_blog_pour_utilisateur
from blog.models import BlogPost


def inscription(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Crée l'utilisateur
            user = form.save()

            # # Crée le blog automatiquement
            # blog = creer_blog_pour_utilisateur(
            #     user=user,
            #     nom_entreprise=form.cleaned_data['nom_entreprise'],
            #     ville=form.cleaned_data['ville'],
            #     secteur=form.cleaned_data['secteur'],
            # )

            # # Lie le blog au profil
            # user.profil.blog = blog
            # user.profil.ville = form.cleaned_data['ville']
            # user.profil.secteur = form.cleaned_data['secteur']
            # user.profil.save()
            
            # donner_droits_wagtail(user, blog)           

            # Connecte l'utilisateur
            login(request, user)
            from core.tasks import envoyer_email_bienvenue

            # Après login(request, user)
            envoyer_email_bienvenue.delay(user.id, blog.title)
            messages.success(
                request,
                f"Bienvenue ! Votre blog est prêt sur /{blog.slug}/"
            )
            return redirect('accounts:dashboard')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect('portfolio:dashboard_portfolio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    return redirect('accounts:connexion')


@login_required
def dashboard(request):
    profil = request.user.profil
    articles = []
    total_vues = 0
    total_likes = 0

    if profil.a_un_blog():
        articles = BlogPost.objects.child_of(
            profil.blog
        ).order_by('-date_publication')
        total_vues = sum(a.vues for a in articles)
        total_likes = sum(a.likes for a in articles)

    return render(request, 'accounts/dashboard.html', {
        'profil': profil,
        'articles': articles,
        'total_vues': total_vues,
        'total_likes': total_likes,
    })

@login_required
def mettre_a_jour_profil(request):
    profil = request.user.profil

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            # Met à jour le profil
            profil.ville = form.cleaned_data['ville']
            profil.secteur = form.cleaned_data['secteur']
            profil.description = form.cleaned_data['description']
            profil.telephone = form.cleaned_data['telephone']
            if form.cleaned_data.get('logo'):
                profil.logo = form.cleaned_data['logo']
            profil.save()

            # Met à jour le blog Wagtail
            if profil.a_un_blog():
                blog = profil.blog
                blog.title = form.cleaned_data['nom_entreprise']
                blog.ville = form.cleaned_data['ville']
                blog.secteur = form.cleaned_data['secteur']
                blog.description = form.cleaned_data['description']
                blog.save_revision().publish()

            return render(request, 'accounts/partials/profil_succes.html')
    else:
        form = ProfilForm(initial={
            'nom_entreprise': profil.blog.title if profil.a_un_blog() else '',
            'ville': profil.ville,
            'secteur': profil.secteur,
            'description': profil.description,
            'telephone': profil.telephone,
        })

    return render(request, 'accounts/partials/profil_form.html', {
        'form': form
    })

from wagtail.models import GroupPagePermission
from django.contrib.auth.models import Group, Permission

def donner_droits_wagtail(user, blog):
    """Donne à l'utilisateur les droits d'édition sur son blog uniquement"""

    # Récupère ou crée un groupe éditeur
    groupe, _ = Group.objects.get_or_create(name=f'editeur_{user.username}')

    # Ajoute l'utilisateur au groupe
    user.groups.add(groupe)

    # Récupère les permissions Wagtail
    permissions = Permission.objects.filter(
        content_type__app_label='wagtailcore',
        codename__in=['add_page', 'change_page', 'publish_page', 'delete_page']
    )

    # Donne les permissions sur son blog uniquement
    for permission in permissions:
        GroupPagePermission.objects.get_or_create(
            group=groupe,
            page=blog,
            permission=permission,
        )

    # Donne accès à l'admin Wagtail
    
    user.is_staff = True
    
    # Permission explicite d'accès à l'admin Wagtail ← nouveau
    wagtail_admin_perm = Permission.objects.get(
        content_type__app_label='wagtailadmin',
        codename='access_admin'
    )
    user.user_permissions.add(wagtail_admin_perm)
    user.save()
####
