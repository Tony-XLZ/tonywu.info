from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blogs.models import Blog
from jobs.models import Job
from photos.models import Photo

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'photos_list']

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

class PhotoSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Photo.objects.filter(is_published=True)
