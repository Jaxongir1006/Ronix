from django.contrib import admin
from .models import AboutUs,FAQ
from parler.admin import TranslatableAdmin

admin.site.register(FAQ)

@admin.register(AboutUs)
class AboutUsAdmin(TranslatableAdmin):
    list_display = ('__str__',)