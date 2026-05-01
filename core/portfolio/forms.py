from django import forms
from .models import Portfolio, Realisation, Service, Temoignage, MessageContact,Statistique
from django.utils.text import slugify
####

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio   
        fields = [
            'titre', 'bio', 'photo',
            'telephone', 'email_contact', 'whatsapp',
            'facebook', 'linkedin', 'instagram',
        ]


class RealisationForm(forms.ModelForm):
    class Meta:
        model = Realisation
        fields = ['titre', 'description', 'image', 'lien', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class TemoignageForm(forms.ModelForm):
    class Meta:
        model = Temoignage
        fields = ['nom_client', 'entreprise', 'contenu', 'note']


class MessageContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'telephone', 'message']
        

class StatistiqueForm(forms.ModelForm):
    class Meta:
        model = Statistique
        fields = ['chiffre', 'label']
        widgets = {
            'chiffre': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200', 'placeholder': 'Ex: 150'}),
            'label': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200', 'placeholder': 'Ex: Clients satisfaits'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['titre', 'description', 'prix', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none', 'rows': 3}),
            'prix': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 outline-none'}),
            # Utilise FileInput au lieu de ClearableFileInput pour HTMX
            'image': forms.FileInput(attrs={'class': 'hidden', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On rend l'image optionnelle pour permettre la modification sans upload systématique
        self.fields['image'].required = False