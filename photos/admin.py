from django.contrib import admin
from django.utils.html import format_html

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'preview',
        'display_title',
        'location',
        'taken_at',
        'is_featured',
        'is_published',
        'display_order',
        'created_at',
    )
    list_editable = ('is_featured', 'is_published', 'display_order')
    list_filter = ('is_published', 'is_featured', 'taken_at', 'created_at')
    search_fields = ('title', 'alt_text', 'description', 'location', 'camera')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    ordering = ('display_order', '-taken_at', '-created_at')
    fieldsets = (
        ('Image', {
            'fields': ('image', 'image_preview', 'title', 'alt_text'),
        }),
        ('Story', {
            'fields': ('description', 'location', 'camera', 'taken_at'),
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'display_order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def preview(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" alt="" style="height: 56px; width: 72px; object-fit: cover; border-radius: 4px;" />',
            obj.image.url,
        )

    preview.short_description = 'Preview'

    def image_preview(self, obj):
        if not obj.image:
            return 'Upload an image to see a preview.'
        return format_html(
            '<img src="{}" alt="" style="max-width: 420px; max-height: 280px; object-fit: contain; border-radius: 6px;" />',
            obj.image.url,
        )

    image_preview.short_description = 'Current image'
