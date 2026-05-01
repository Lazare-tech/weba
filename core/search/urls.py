from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import search.views
app_name = "search"
##
urlpatterns = [
      path('', search.views.index, name='index'),
    path('recherche/', search.views.recherche, name='recherche'),
     path('ajouter/', search.views.ajouter, name='ajouter'),
    path('liste/', search.views.liste_complete, name='liste'),
    path('supprimer/<int:pk>/', search.views.supprimer, name='supprimer'),
] +   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)