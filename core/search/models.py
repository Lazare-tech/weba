from django.db import models

# Create your models here.
from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    secteur = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)

    def __str__(self):
        return self.nom