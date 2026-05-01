from django.contrib.sitemaps import Sitemap
from wagtail.models import Page
from blog.models import BlogIndexPage, BlogPost


class BlogIndexSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogIndexPage.objects.live().public()

    def location(self, obj):
        return obj.full_url.replace('http://localhost:8000', '')

    def lastmod(self, obj):
        return obj.latest_revision_created_at


class BlogPostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return BlogPost.objects.live().public()

    def location(self, obj):
        return obj.full_url.replace('http://localhost:8000', '')

    def lastmod(self, obj):
        return obj.latest_revision_created_at