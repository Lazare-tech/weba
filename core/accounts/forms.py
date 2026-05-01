from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription minimaliste"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email'] # Les mots de passe sont gérés par UserCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprime les textes d'aide par défaut de Django (ex: "Le mot de passe doit contenir...")
        for field in self.fields.values():
            field.help_text = None

class ProfilForm(forms.Form):
    """Formulaire de mise à jour du profil"""
    nom_entreprise = forms.CharField(max_length=200)
    ville = forms.CharField(max_length=100)
    secteur = forms.CharField(max_length=100)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    telephone = forms.CharField(max_length=20, required=False)
    logo = forms.ImageField(required=False)