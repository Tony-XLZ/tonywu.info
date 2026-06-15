from django.shortcuts import render, get_object_or_404

from blogs.models import Blog
from photos.models import Photo

from .models import Job


def home(request):
    jobs = Job.objects.all().order_by('-published_date')[:3]
    blogs = Blog.objects.all().order_by('-published_date')[:4]
    photos = Photo.objects.filter(is_published=True).order_by('display_order', '-taken_at', '-created_at')[:5]

    return render(request, 'jobs/home.html', {
        'jobs': jobs,
        'blogs': blogs,
        'photos': photos,
    })


def jobs_list(request):
    jobs = Job.objects.all().order_by('-published_date')
    return render(request, 'jobs/jobs_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/detail.html', {'job': job})
