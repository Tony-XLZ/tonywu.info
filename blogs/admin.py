from django.contrib import admin
from .models import Blog, Category, Tag


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category')
    list_filter = ('published_date', 'category', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
