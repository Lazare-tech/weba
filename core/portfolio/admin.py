from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    Portfolio, Realisation, Service, 
    Temoignage, MessageContact, 
    CategorieTemplate, TemplateMetadata
)

# --- INLINES ---
# Permet de modifier les réalisations et services directement dans la page du Portfolio

class RealisationInline(admin.TabularInline):
    model = Realisation
    extra = 1
    fields = ('titre', 'ordre', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;"/>', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Aperçu"

class ServiceInline(admin.StackedInline):
    model = Service
    extra = 1
    classes = ('collapse',) # Masqué par défaut pour ne pas surcharger la page

# --- CONFIGURATIONS PRINCIPALES ---

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'titre', 'template_badge', 'publie', 'date_creation', 'view_on_site_link')
    list_filter = ('template_choisi', 'publie', 'date_creation')
    search_fields = ('user__username', 'titre', 'slug')
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [RealisationInline, ServiceInline]
    
    # Organisation des champs par sections
    fieldsets = (
        ('Utilisateur & Identité', {
            'fields': ('user', 'slug', 'publie')
        }),
        ('Contenu du Site', {
            'fields': ('titre', 'bio', 'photo'),
        }),
        ('Design & Branding', {
            'classes': ('wide',),
            'fields': (('template_choisi', 'police', 'rayon_bordure'), 
                       ('couleur_primaire', 'couleur_accent'), 
                       ('couleur_fond', 'couleur_fond_2', 'couleur_texte')),
        }),
        ('Contact & Réseaux Sociaux', {
            'classes': ('collapse',),
            'fields': (('telephone', 'whatsapp', 'email_contact'), 
                       ('facebook', 'linkedin', 'instagram')),
        }),
    )

    def template_badge(self, obj):
        color = "#10b981" if obj.template_choisi == 'minimal_blanc' else "#3b82f6"
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 10px; font-weight: bold;">{}</span>',
            color, obj.get_template_choisi_display()
        )
    template_badge.short_description = "Template"

    def view_on_site_link(self, obj):
        return format_html('<a href="{}" target="_blank">🌐 Voir le site</a>', obj.get_absolute_url())
    view_on_site_link.short_description = "Lien Direct"


@admin.register(TemplateMetadata)
class TemplateMetadataAdmin(admin.ModelAdmin):
    list_display = ('preview_thumb', 'nom', 'categorie', 'badge_premium', 'prix_cfa', 'slug_technique')
    list_editable = ('prix_cfa',) # Permet de changer les prix directement dans la liste
    list_filter = ('categorie', 'est_premium')
    search_fields = ('nom', 'slug_technique')
    
    fieldsets = (
        ('Informations Commerciales', {
            'fields': ('nom', 'slug', 'categorie', 'image_preview', 'description_longue')
        }),
        ('Tarification', {
            'fields': (('est_premium', 'prix_cfa', 'slug_technique'),)
        }),
        ('Design d\'Usine (Démo)', {
            'description': "Ces réglages sont appliqués lors de la prévisualisation du template.",
            'fields': (('couleur_primaire', 'couleur_accent'), 
                       ('couleur_fond', 'couleur_fond_2', 'couleur_texte'),
                       ('police_nom', 'police_url', 'rayon_bordure')),
        }),
    )

    def preview_thumb(self, obj):
        if obj.image_preview:
            return format_html('<img src="{}" style="height: 40px; border-radius: 4px;"/>', obj.image_preview.url)
        return "Aucun"
    preview_thumb.short_description = "Aperçu"

    def badge_premium(self, obj):
        if obj.est_premium:
            return format_html('<b style="color: #d97706;">💎 PREMIUM</b>')
        return format_html('<span style="color: #059669;">GRATUIT</span>')
    badge_premium.short_description = "Type"


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom_client', 'portfolio', 'note_stars', 'approuve', 'date')
    list_filter = ('approuve', 'note')
    actions = ['approuver_temoignages']

    def note_stars(self, obj):
        return format_html('{}', '⭐' * obj.note)
    note_stars.short_description = "Note"

    def approuver_temoignages(self, request, queryset):
        queryset.update(approuve=True)
    approuver_temoignages.short_description = "Approuver les témoignages sélectionnés"


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'portfolio', 'date', 'status_lu')
    list_filter = ('lu', 'date')
    readonly_fields = ('nom', 'email', 'telephone', 'message', 'date', 'portfolio')

    def status_lu(self, obj):
        if obj.lu:
            return format_html('<span style="color: green;">✔ Lu</span>')
        return format_html('<b style="color: red;">✉ Nouveau</b>')
    status_lu.short_description = "Status"


@admin.register(CategorieTemplate)
class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nom',)}

# Enregistrement simple pour les autres
admin.site.register(Service)
admin.site.register(Realisation)