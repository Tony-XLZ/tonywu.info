from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.
def blogs_list(request):
    blogs = Blog.objects.all().order_by('-published_date')
    return render(request, 'blogs/blogs_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blogs/detail.html', {'blog': blog})
