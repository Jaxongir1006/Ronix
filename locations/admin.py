from django.contrib import admin
from .models import Branch
from parler.admin import TranslatableAdmin

@admin.register(Branch)
class BranchAdmin(TranslatableAdmin):
    list_display = ('__str__',)