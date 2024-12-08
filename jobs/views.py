from django.shortcuts import render, get_object_or_404
from.models import Job
from blogs.models import Blog

# Create your views here.
def home(request):
    jobs = Job.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'jobs/home.html', {'jobs': jobs, 'blogs': blogs})

def jobs_list(request):
    jobs = Job.objects.all().order_by('-published_date')
    return render(request, 'jobs/jobs_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/detail.html', {'job': job})
