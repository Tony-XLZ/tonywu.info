"""
URL configuration for Portfolio_with_Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
import jobs.views
import blogs.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from sitemap import StaticViewSitemap, BlogSitemap, ProjectSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blogs': BlogSitemap,
    'projects': ProjectSitemap,
}

urlpatterns = [
    path("secret-admin-panel-tonyxlz/", admin.site.urls),
    path("", jobs.views.home, name="home"),
    path('jobs/<int:job_id>/', jobs.views.detail, name="detail"),
    path('blogs/<int:blog_id>/', blogs.views.blog_detail, name="blog_detail"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
