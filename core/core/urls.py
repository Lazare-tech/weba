"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
#
from django.views.generic import TemplateView

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    ), name='robots'),
]
#
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('weba-admin/', include(wagtailadmin_urls)),
    path('pages/', include(wagtail_urls)),
    path('', include('search.urls')),
    # path('blog/', include('blog.urls')),
    path('', include('accounts.urls')),
    path('', include('abonnements.urls')),
    path('', include('analytics.urls')),
    # path('', include('seo.urls')),
    path('', include('portfolio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)