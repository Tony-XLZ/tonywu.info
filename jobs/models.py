from django.db import models
from django.urls import reverse

# Create your models here.
class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    summary = models.CharField(max_length=400)
    detail = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.summary

    def get_absolute_url(self):
        return reverse('job_detail', args=[self.id])
