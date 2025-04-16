from django.contrib import admin
from .models import Product, Category, Specification,SubCategory,ProductImages
from parler.admin import TranslatableAdmin

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('__str__',)

@admin.register(SubCategory)
class SubCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__',)

admin.site.register(Specification)

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('__str__',)

admin.site.register(ProductImages)

