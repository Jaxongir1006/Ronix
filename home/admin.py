from django.contrib import admin
from .models import HomeBanner
from parler.admin import TranslatableAdmin

@admin.register(HomeBanner)
class HomeBannerAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    list_filter = ('translations__title',)
    search_fields = ('translations__title',)
