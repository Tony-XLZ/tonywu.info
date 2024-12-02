from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blogs.models import Blog
from jobs.models import Job

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Blog.objects.all()

class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Job.objects.all()
