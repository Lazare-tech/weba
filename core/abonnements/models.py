from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """Définition des plans disponibles"""
    NOM_CHOICES = [
        ('gratuit', 'Gratuit'),
        ('pro', 'Pro'),
        ('business', 'Business'),
    ]
    nom = models.CharField(max_length=20, choices=NOM_CHOICES, unique=True)
    prix_mensuel = models.PositiveIntegerField(default=0)  # en FCFA
    description = models.TextField(blank=True)

    # Limites et fonctionnalités
    templates_premium = models.BooleanField(default=False)
    analytics_avances = models.BooleanField(default=False)
    portfolio = models.BooleanField(default=False)
    ia_branding = models.BooleanField(default=False)
    app_web = models.BooleanField(default=False)
    automatisations = models.BooleanField(default=False)
    portfolio_equipe = models.BooleanField(default=False)

    def __str__(self):
        return self.get_nom_display()

    class Meta:
        verbose_name = "Plan"


class Abonnement(models.Model):
    """Abonnement actif d'un utilisateur"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='abonnement'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='abonnes'
    )
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    # Référence paiement (Wave, Orange Money, etc.)
    reference_paiement = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.plan}"

    def est_actif(self):
        from django.utils import timezone
        if not self.actif:
            return False
        if self.date_fin and self.date_fin < timezone.now():
            return False
        return True

    class Meta:
        verbose_name = "Abonnement"


class DemandeUpgrade(models.Model):
    """Demande de passage à un plan supérieur"""
    STATUTS = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('refuse', 'Refusé'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_demande = models.ForeignKey(Plan, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    reference_paiement = models.CharField(
        max_length=200,
        blank=True,
        help_text="Référence du paiement Wave/Orange Money"
    )
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} → {self.plan_demande} ({self.statut})"

    class Meta:
        verbose_name = "Demande d'upgrade"
        ordering = ['-date_demande']