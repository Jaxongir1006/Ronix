from django.contrib import admin
from .models import HomeBanner, CustomerReview
from parler.admin import TranslatableAdmin

class HomeBannerAdmin(TranslatableAdmin):
    list_display = ('__str__', 'imageURL')
    list_filter = ('translations__title',)
    search_fields = ('translations__title',)
