from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import Page
# from blog.models import BlogIndexPage


class ProfilUtilisateur(models.Model):
    """Profil lié à chaque utilisateur Django"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil'
    )
    # blog = models.OneToOneField(
    #     BlogIndexPage,
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True,
    #     related_name='proprietaire'
    # )
    telephone = models.CharField(max_length=20, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    secteur = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='logos/',
        null=True, blank=True
    )
    # Plan d'abonnement
    PLANS = [
        ('gratuit', 'Gratuit'),
        ('pro', 'Pro'),
        ('business', 'Business'),
    ]
    plan = models.CharField(
        max_length=20,
        choices=PLANS,
        default='gratuit'
    )

    def __str__(self):
        return f"Profil de {self.user.username}"

    def a_un_blog(self):
        return self.blog is not None


# def creer_blog_pour_utilisateur(user, nom_entreprise, ville, secteur):
#     """Crée automatiquement un blog Wagtail pour un utilisateur"""
#     from django.utils.text import slugify

#     # Page racine de Wagtail
#     root = Page.objects.get(id=1)

#     # Slug unique
#     slug_base = slugify(nom_entreprise)
#     slug = slug_base
#     compteur = 1
#     while Page.objects.filter(slug=slug).exists():
#         slug = f"{slug_base}-{compteur}"
#         compteur += 1

#     # Crée le blog
#     blog = BlogIndexPage(
#         title=nom_entreprise,
#         slug=slug,
#         ville=ville,
#         secteur=secteur,
#         description=f"Blog de {nom_entreprise}",
#     )
#     root.add_child(instance=blog)
#     blog.save_revision().publish()

#     return blog


@receiver(post_save, sender=User)
def creer_profil(sender, instance, created, **kwargs):
    """Crée automatiquement un profil quand un utilisateur est créé"""
    if created:
        ProfilUtilisateur.objects.create(user=instance)