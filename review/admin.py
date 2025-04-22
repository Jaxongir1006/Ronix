from django.contrib import admin
from .models import Review,Rate,CustomerReview
from parler.admin import TranslatableAdmin

admin.site.register(Review)
admin.site.register(Rate)

@admin.register(CustomerReview)
class CustomerReviewAdmin(TranslatableAdmin):
    list_display = ('__str__', 'videoURL')
    list_filter = ('translations__title',)
    search_fields = ('translations__title',)