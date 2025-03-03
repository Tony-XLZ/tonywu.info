from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    alt_text = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alt_text or f'Photo {self.id}'
