from django.db import models
from django.urls import reverse
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import os
# --- CONFIGURATION & CONSTANTES ---

POLICES = [
    ('inter',    'Inter — Moderne'),
    ('georgia',  'Georgia — Classique'),
    ('poppins',  'Poppins — Arrondi'),
    ('playfair', 'Playfair — Luxe'),
    ('mono',     'Monospace — Tech'),
]

RAYONS = [
    ('0px',    'Carré — Strict'),
    ('6px',    'Légèrement arrondi'),
    ('12px',   'Arrondi — Standard'),
    ('20px',   'Très arrondi'),
    ('9999px', 'Pill — Maximal'),
]

PALETTES_DEFAUT = {
    'afrique_moderne': {'couleur_primaire': '#1D9E75', 'couleur_accent': '#EF9F27', 'couleur_fond': '#04342C', 'couleur_fond_2': '#085041', 'couleur_texte': '#E1F5EE'},
    'minimal_blanc':   {'couleur_primaire': '#042C53', 'couleur_accent': '#185FA5', 'couleur_fond': '#ffffff', 'couleur_fond_2': '#F1EFE8', 'couleur_texte': '#2C2C2A'},
    'bold_coral':      {'couleur_primaire': '#D85A30', 'couleur_accent': '#993C1D', 'couleur_fond': '#FAFAF8', 'couleur_fond_2': '#FAECE7', 'couleur_texte': '#2C2C2A'},
    'tech_purple':     {'couleur_primaire': '#7F77DD', 'couleur_accent': '#5DCAA5', 'couleur_fond': '#26215C', 'couleur_fond_2': '#3C3489', 'couleur_texte': '#EEEDFE'},
    'onyx_impact':     {'couleur_primaire': '#C9A84C', 'couleur_accent': '#EF9F27', 'couleur_fond': '#0A0A0A', 'couleur_fond_2': '#111111', 'couleur_texte': '#F5F5F5'},
}

# --- MODELES ---


def user_directory_path(instance, filename):
    # Si l'instance a directement un attribut 'user', c'est le Portfolio
    if hasattr(instance, 'user'):
        user_id = instance.user.id
        folder = "profil"
    # Sinon, on remonte via le lien portfolio (Service ou Realisation)
    else:
        user_id = instance.portfolio.user.id
        folder = "services" if isinstance(instance, Service) else "realisations"
    
    return f'user_{user_id}/{folder}/{filename}'
class Portfolio(models.Model):
    """Portfolio principal d'un utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    est_personnalise = models.BooleanField(default=False)
    # --- Infos personnelles ---
    titre = models.CharField(max_length=200, help_text="Ex: Menuisier professionnel à Ouagadougou")
    bio = models.TextField(blank=True, help_text="Présentation détaillée de votre activité")
    photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    # --- Configuration du Design ---
    CHOIX_TEMPLATES = [
        ('minimal_blanc', 'Minimaliste (Expert)'),
        ('bold_coral','Bold Coral (Premium)'),
        ('tech_slate', 'Tech Slate (Premium)'),
        ('creative_can', 'Creative Can (Premium)'),
        ('tera_decor','Tera Decor (Premium)'),
        ('prestige_events','Prestige Events(Premium)'),
    ]
    template_choisi = models.CharField(max_length=50, choices=CHOIX_TEMPLATES, default='minimal_blanc')
    
    couleur_primaire = models.CharField(max_length=7, blank=True,null=True)
    couleur_accent   = models.CharField(max_length=7, blank=True,null=True)
    couleur_fond     = models.CharField(max_length=7, blank=True,null=True)
    couleur_fond_2   = models.CharField(max_length=7, blank=True,null=True)
    couleur_texte    = models.CharField(max_length=7, blank=True,null=True)
    police           = models.CharField(max_length=50, choices=POLICES, default='inter')
    rayon_bordure    = models.CharField(max_length=10, choices=RAYONS, default='12px')

    # --- Contact ---
    telephone     = models.CharField(max_length=20, blank=True)
    email_contact = models.EmailField(blank=True)
    whatsapp      = models.CharField(max_length=20, blank=True)
    facebook      = models.URLField(blank=True)
    linkedin      = models.URLField(blank=True)
    instagram     = models.URLField(blank=True)

    # --- Paramètres techniques ---
    slug          = models.SlugField(unique=True)
    publie        = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Portfolio"

    def __str__(self):
        return f"Portfolio de {self.user.username}"

    def get_absolute_url(self):
        return reverse('portfolio:portfolio_public', args=[self.slug])

    def appliquer_palette_defaut(self):
        palette = PALETTES_DEFAUT.get(self.template_choisi, {})
        for champ, valeur in palette.items():
            setattr(self, champ, valeur)

    def get_police_family(self):
        families = {
            'inter': "'Inter', sans-serif",
            'georgia': "Georgia, serif",
            'poppins': "'Poppins', sans-serif",
            'playfair': "'Playfair Display', serif",
            'mono': "'JetBrains Mono', monospace",
        }
        return families.get(self.police, "'Inter', sans-serif")
    def get_police_url(self):
        """Retourne l'URL Google Fonts correspondant à la police choisie"""
        urls = {
            'inter':    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            'poppins':  "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            'playfair': "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap",
            'mono':     "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap",
        }
        # Retourne l'URL ou None si c'est une police système (comme Georgia)
        return urls.get(self.police)
    
    def get_absolute_url(self):
        # Assure-toi que 'portfolio:portfolio_public' correspond à ton urls.py
        return reverse('portfolio:portfolio_public_preview', args=[self.slug])
    @property
    def est_theme_premium(self):
        return self.template_choisi not in ['minimal_blanc']

    @property
    def THEMES_CHOICES(self):
        return self.CHOIX_TEMPLATES

class Realisation(models.Model):
    """Projet ou réalisation dans le portfolio"""
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='realisations'
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
   
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    lien = models.URLField(blank=True)
    date = models.DateField(null=True, blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', '-date']
        verbose_name = "Réalisation"

    def __str__(self):
        return self.titre
class Statistique(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stats')
    chiffre = models.CharField(default="10",max_length=20, help_text="Ex: 150, 10, 24k",null=True,blank=True)
    label = models.CharField(max_length=100, help_text="Ex: Mariages, Ans d'Expérience",null=True,blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.chiffre} {self.label}"

class Service(models.Model):
    """Service proposé dans le portfolio"""
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='services'
    )
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ex: À partir de 5 000 FCFA"
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Service"

    def __str__(self):
        return self.titre


class Temoignage(models.Model):
    """Avis client"""
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='temoignages'
    )
    nom_client = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100, blank=True)
    contenu = models.TextField()
    note = models.PositiveIntegerField(
        default=5,
        choices=[(i, i) for i in range(1, 6)]
    )
    approuve = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Témoignage"

    def __str__(self):
        return f"{self.nom_client} → {self.portfolio}"


class MessageContact(models.Model):
    """Message reçu via le formulaire de contact du portfolio"""
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True,null=True)
    sujet = models.CharField(max_length=200, default="Demande de contact") 
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Message de contact"

    def __str__(self):
        return f"{self.nom} → {self.portfolio}"
# --- NOUVEAUX MODELES ---

class CategorieTemplate(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

class TemplateMetadata(models.Model):
    """Stocke les infos de vente/démo des templates"""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # ex: tech-slate
    categorie = models.ForeignKey(CategorieTemplate, on_delete=models.SET_NULL, null=True, related_name='templates')
    image_preview = models.ImageField(upload_to='templates/previews/')
    description_longue = models.TextField()
    est_premium = models.BooleanField(default=False)
    prix_cfa = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    # Pour le bouton "Appliquer"
    slug_technique = models.CharField(max_length=50, help_text="Le nom utilisé dans Portfolio.CHOIX_TEMPLATES")

    # Réglages de design par défaut (pour la démo)
    couleur_primaire = models.CharField(max_length=20, default="#10b981") # Emerald-500
    couleur_accent = models.CharField(max_length=20, default="#059669")
    couleur_fond = models.CharField(max_length=20, default="#ffffff")
    couleur_fond_2 = models.CharField(max_length=20, default="#f8fafc")
    couleur_texte = models.CharField(max_length=20, default="#0f172a")
    
    police_nom = models.CharField(max_length=100, default="Inter")
    police_url = models.URLField(blank=True, null=True) # Lien Google Fonts
    rayon_bordure = models.CharField(max_length=20, default="0.75rem")
    
    def __str__(self):
        return self.nom