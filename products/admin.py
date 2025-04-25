from django.contrib import admin
from .models import Product, Category, Specification,SubCategory,ProductImages,ProductDetail
from parler.admin import TranslatableAdmin

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    search_fields = ('translations__name',)
    list_filter = ('translations__name',)

@admin.register(SubCategory)
class SubCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__', 'category')
    search_fields = ('translation__name',)
    list_filter = ('category', 'parent', 'translation__name')


@admin.register(Specification)
class SpecificationAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    search_fields = ('translations__type',)

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('__str__', 'subcategory')
    search_fields = ('translations__name',)
    list_filter = ('subcategory', 'translations__name')

admin.site.register(ProductImages)

@admin.register(ProductDetail)
class ProductDetailAdmin(TranslatableAdmin):
    list_display = ('__str__',)
    search_fields = ('translations__title',)
    list_filter = ('translations__title',)
