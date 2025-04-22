from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Series, SeriesCategory, SeriesCategoryDetail

@admin.register(Series)
class SeriesAdmin(TranslatableAdmin):
    list_display = ('__str__', 'image_preview')
    search_fields = ('translations__name',)
    
    def image_preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='50' height='50' />"
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

@admin.register(SeriesCategory)
class SeriesCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__', 'series', 'media_type')
    list_filter = ('series', 'translations__title')
    search_fields = ('translations__title', 'translations__name')
    
    def media_type(self, obj):
        if obj.image:
            return "Image"
        elif obj.video:
            return "Video"
        return "None"
    media_type.short_description = "Media Type"

@admin.register(SeriesCategoryDetail)
class SeriesCategoryDetailAdmin(TranslatableAdmin):
    list_display = ('__str__', 'category', 'has_image', 'has_video')
    list_filter = ('category',)
    search_fields = ('translations__title',)

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image"

    def has_video(self, obj):
        return bool(obj.video)
    has_video.boolean = True
    has_video.short_description = "Video"
