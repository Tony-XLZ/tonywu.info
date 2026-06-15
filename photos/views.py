from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Photo


def photos_list(request):
    photos = Photo.objects.filter(is_published=True)
    featured_photos = photos.filter(is_featured=True)[:3]
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'photos/photos_list.html', {
        'page_obj': page_obj,
        'featured_photos': featured_photos,
    })


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, is_published=True)
    nearby_photos = Photo.objects.filter(is_published=True).exclude(pk=photo.pk)[:4]

    return render(request, 'photos/detail.html', {
        'photo': photo,
        'nearby_photos': nearby_photos,
    })
