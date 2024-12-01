from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
