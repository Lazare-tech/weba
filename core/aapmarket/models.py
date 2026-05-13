from django.db import models
from django.utils.text import slugify
# Create your models here.

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    reponse = models.TextField()
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        ordering = ['ordre']

    def __str__(self):
        return self.question
###
class ContactMessage(models.Model):
    TYPE_CHOICES = [
        ('PARTENARIAT', 'Partenariat École'),
        ('SUPPORT', 'Support Technique'),
        ('DEVIS', 'Demande de Devis'),
        ('AUTRE', 'Autre'),
    ]
    
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    type_demande = models.CharField(max_length=20, choices=TYPE_CHOICES, default='AUTRE')
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message de Contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} - {self.type_demande}"
####
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Abonné Newsletter"

    def __str__(self):
        return self.email
#####
class BlogPost(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image_couverture = models.ImageField(upload_to='blog/covers/', null=True, blank=True)
    contenu = models.TextField()
    extrait = models.TextField(help_text="Petit texte pour l'aperçu sur la carte.")
    
    # Meta SEO
    meta_description = models.CharField(max_length=160, blank=True)
    score_seo = models.IntegerField(default=0) # Pour l'affichage 98% sur tes cartes
    
    date_publication = models.DateTimeField(auto_now_add=True)
    est_publie = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Article de Blog"
        ordering = ['-date_publication']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre