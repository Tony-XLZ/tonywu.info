from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from uuslug import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

    def __str__(self):
        return self.name

    def get_all_blogs(self):
        """Returns all blogs in this category and its subcategories."""
        all_categories = [self] + list(self.get_descendants())
        return Blog.objects.filter(category__in=all_categories)

    def get_descendants(self):
        """Recursively fetch all descendant categories."""
        descendants = []
        subcategories = self.subcategories.all()
        for subcategory in subcategories:
            descendants.append(subcategory)
            descendants.extend(subcategory.get_descendants())
        return descendants

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail', args=[self.slug])

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name='blogs', on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.id])

    def get_category_tree(self):
        """Returns the category tree for this blog's category."""
        category = self.category
        tree = []
        while category:
            tree.append(category)
            category = category.parent_category
        return tree[::-1]  # Reverse to get root-to-leaf order
