from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class HomePageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['Ranker:home']

    def location(self, item):
        return reverse(item)

class AboutPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return ['Ranker:about_page']

    def location(self, item):
        return reverse(item)

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['Ranker:login_page', 'Ranker:sign_up']

    def location(self, item):
        return reverse(item)