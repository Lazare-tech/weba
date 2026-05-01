from django import forms
from .models import Entreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom', 'secteur', 'ville']