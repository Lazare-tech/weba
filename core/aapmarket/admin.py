
from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber, BlogPost,FAQ
# Register your models here.

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'type_demande', 'date_envoi', 'est_lu')
    list_filter = ('type_demande', 'est_lu', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    list_editable = ('est_lu',) # Permet de cocher "lu" directement dans la liste
    readonly_fields = ('date_envoi',)

@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_inscription', 'est_actif')
    list_filter = ('est_actif', 'date_inscription')
    search_fields = ('email',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'est_publie', 'score_seo')
    list_filter = ('est_publie', 'date_publication')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)} # Génère le slug en temps réel
    list_editable = ('est_publie', 'score_seo')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    # Affichage des colonnes dans la liste
    list_display = ('question', 'ordre', 'reponse_preview')
    
    # Permet de modifier l'ordre directement dans la liste sans ouvrir chaque objet
    list_editable = ('ordre',)
    
    # Barre de recherche pour retrouver rapidement une question
    search_fields = ('question', 'reponse')
    
    # Tri par défaut basé sur le champ ordre défini dans Meta
    ordering = ('ordre',)

    def reponse_preview(self, obj):
        """Affiche un aperçu court de la réponse dans l'admin."""
        if len(obj.reponse) > 50:
            return f"{obj.reponse[:50]}..."
        return obj.reponse
    
    reponse_preview.short_description = "Aperçu de la réponse"