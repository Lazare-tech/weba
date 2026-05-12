from django.views.generic import TemplateView, ListView
from .models import FAQ




# ==========================================
# 1. PLATEFORME (Produit & démo)
# ==========================================

class TemplatesView(TemplateView):
    """Galerie des modèles de portfolio"""
    template_name = "aapmarket/body/index.html"

class BlogEngineView(TemplateView):
    """Présentation du moteur de blog no-code"""
    template_name = "aapmarket/blog_engine.html"


class TarifsView(TemplateView):
    """Grille tarifaire (Initial, Pro, Institution)"""
    template_name = "aapmarket/pricing.html"

class DemoView(TemplateView):
    """Page de démonstration interactive"""
    template_name = "aapmarket/demo.html"


# ==========================================
# 2. ENTREPRISE (Vision & Marque)
# ==========================================
class ServicesView(TemplatesView):
    """Présentation des services de WEBA"""
    template_name = "aapmarket/services.html"

class BlogView(TemplateView):
    """Présentation du blog de WEBA avec effet Skeleton si vide"""
    template_name = "aapmarket/blog.html"

    def get_context_data(self, **kwargs):
        # Appeler le contexte parent
        context = super().get_context_data(**kwargs)
        
        # Simulation d'absence d'articles
        articles = [] 
        
        # Injection des variables dans le contexte
        context['articles'] = articles
        context['is_loading'] = True  # Déclenche le Shimmer dans le template
        
        return context
    
class BlogDetailView(TemplateView):
    """Détails d'un article de blog"""
    template_name = "aapmarket/blog_detail_article.html"
    
class AProposView(TemplateView):
    """Histoire de WEBA et lien avec UNI"""
    template_name = "aapmarket/about.html"

class AccelerateurView(TemplateView):
    """Partenariats écoles et incubateurs"""
    template_name = "aapmarket/accelerator.html"

class CareersView(TemplateView):
    """Opportunités de recrutement"""
    template_name = "aapmarket/careers.html"

class PressView(TemplateView):
    """Espace presse et kit média"""
    template_name = "aapmarket/press.html"


# ==========================================
# 3. SUPPORT & LÉGAL
# ==========================================

class ContactView(TemplateView):
    """Formulaire de contact et support"""
    template_name = "aapmarket/contact.html"

class FAQView(ListView):
    """Foire aux questions dynamique"""
    model = FAQ
    template_name = "aapmarket/faq.html"
    context_object_name = "faqs"

class LegalView(TemplateView):
    """Mentions légales"""
    template_name = "aapmarket/legal_mention.html"

class PrivacyView(TemplateView):
    """Politique de confidentialité"""
    template_name = "aapmarket/privacy.html"