from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogIndexSitemap, BlogPostSitemap
from . import views

sitemaps = {
    'blogs': BlogIndexSitemap,
    'articles': BlogPostSitemap,
}

urlpatterns = [
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('seo/score/<int:page_id>/', views.score_seo_article, name='score_seo_article'),
    path('seo/blog/', views.score_seo_blog, name='score_seo_blog'),
]