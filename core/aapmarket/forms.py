from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'type_demande', 'message']
        # On définit les widgets pour correspondre exactement à ton design HTML
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full p-4 bg-[var(--bg-alt)] rounded-xl border border-transparent focus:border-[var(--brand-primary)] focus:bg-white outline-none transition-all',
                'placeholder': 'Ex: Jean Traoré'
            }),
            'type_demande': forms.Select(attrs={
                'class': 'w-full p-4 bg-[var(--bg-alt)] rounded-xl border border-transparent focus:border-[var(--brand-primary)] focus:bg-white outline-none transition-all appearance-none'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-4 bg-[var(--bg-alt)] rounded-xl border border-transparent focus:border-[var(--brand-primary)] focus:bg-white outline-none transition-all',
                'placeholder': 'nom@entreprise.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full p-4 bg-[var(--bg-alt)] rounded-xl border border-transparent focus:border-[var(--brand-primary)] focus:bg-white outline-none transition-all',
                'placeholder': 'Dites-nous comment nous pouvons vous aider...',
                'rows': 4
            }),
        }

    # Vérification personnalisée : Longueur du message
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Le message est trop court. Soyez plus précis.")
        return message

    # Vérification personnalisée : Blocage de domaines suspects (Anti-Spam)
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        domaine_bloque = ['temp-mail.org', 'guerrillamail.com']
        domaine = email.split('@')[-1]
        if domaine in domaine_bloque:
            raise forms.ValidationError("Les adresses email temporaires ne sont pas acceptées.")
        return email