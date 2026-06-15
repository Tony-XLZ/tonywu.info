from django.db import models
from django.urls import reverse

class Photo(models.Model):
    title = models.CharField(max_length=160, blank=True)
    image = models.ImageField(upload_to='photos/')
    alt_text = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    camera = models.CharField(max_length=120, blank=True)
    taken_at = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['display_order', '-taken_at', '-created_at']

    def __str__(self):
        return self.title or self.alt_text or f'Photo {self.id}'

    def get_absolute_url(self):
        return reverse('photo_detail', args=[self.id])

    @property
    def display_title(self):
        return self.title or self.alt_text or 'Untitled photo'

    @property
    def display_alt_text(self):
        return self.alt_text or self.display_title
