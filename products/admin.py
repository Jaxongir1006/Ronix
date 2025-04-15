from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Product, Category, Specification


# @admin.register(Category)
# class CategoryAdmin(TranslationAdmin):
#     list_display = ('name', 'description')

# @admin.register(Product)
# class ProductAdmin(TranslationAdmin):
#     list_display = ('name', 'description', 'features', 'category')


admin.site.register(Specification)
admin.site.register(Category)
admin.site.register(Product)

