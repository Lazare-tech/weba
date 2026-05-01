from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
# from blog.models import BlogPost
from .analyzer import analyser_seo


# @login_required
# def score_seo_article(request, page_id):
#     """Retourne le score SEO d'un article via HTMX"""
#     post = get_object_or_404(BlogPost, id=page_id)

#     # Vérifie que l'article appartient à l'utilisateur
#     if not request.user.profil.a_un_blog():
#         return HttpResponse("Non autorisé", status=403)

#     if post.get_parent().specific != request.user.profil.blog:
#         return HttpResponse("Non autorisé", status=403)

#     resultat = analyser_seo(
#         titre=post.title,
#         description=post.intro,
#         corps=post.corps,
#         tags=post.tags,
#     )

#     from django.shortcuts import render
#     return render(request, 'seo/partials/score_seo.html', {
#         'resultat': resultat,
#         'post': post,
#     })


# @login_required
# def score_seo_blog(request):
#     """Score SEO global du blog de l'utilisateur"""
#     profil = request.user.profil

#     if not profil.a_un_blog():
#         from django.shortcuts import render
#         return render(request, 'seo/partials/score_seo_blog.html', {
#             'score': 0,
#             'conseils': ["Créez votre blog pour obtenir votre score SEO"]
#         })

#     blog = profil.blog
#     conseils = []
#     score = 0

#     # Vérifie description du blog
#     if blog.description:
#         score += 25
#         if len(blog.description) < 100:
#             conseils.append("Description du blog trop courte — visez 100+ caractères")
#     else:
#         conseils.append("Ajoutez une description à votre blog")

#     # Vérifie ville et secteur
#     if blog.ville:
#         score += 25
#     else:
#         conseils.append("Ajoutez votre ville pour le référencement local")

#     if blog.secteur:
#         score += 25
#     else:
#         conseils.append("Ajoutez votre secteur d'activité")

#     # Vérifie le nombre d'articles
#     from blog.models import BlogPost
#     nb_articles = BlogPost.objects.child_of(blog).live().count()
#     if nb_articles >= 5:
#         score += 25
#     elif nb_articles >= 1:
#         score += 10
#         conseils.append(
#             f"Publiez plus d'articles ({nb_articles} actuellement) — visez 5 minimum"
#         )
#     else:
#         conseils.append("Publiez votre premier article pour améliorer votre SEO")

#     from django.shortcuts import render
#     from .analyzer import get_niveau
#     return render(request, 'seo/partials/score_seo_blog.html', {
#         'score': score,
#         'niveau': get_niveau(score),
#         'conseils': conseils,
#         'nb_articles': nb_articles,
#     })