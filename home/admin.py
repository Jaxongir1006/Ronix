from django.contrib import admin
from .models import HomeBanner,CustomerReview
from parler.admin import TranslatableAdmin

@admin.register(HomeBanner)
class HomeBannerAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    list_filter = ('translations__title',)
    search_fields = ('translations__title',)

@admin.register(CustomerReview)
class CustomerReviewAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    list_filter = ('translations__title',)
    search_fields = ('translations__title',)