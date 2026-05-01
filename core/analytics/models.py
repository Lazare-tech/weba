from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class SitePlausible(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='site_plausible'
    )
    domaine = models.CharField(max_length=200)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.domaine}"

    class Meta:
        verbose_name = "Site Plausible"