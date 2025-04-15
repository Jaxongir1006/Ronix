from modeltranslation.translator import translator, TranslationOptions,register
from .models import Product, Category

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'features', 'description')
# translator.register(Product, ProductTranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
# translator.register(Category, CategoryTranslationOptions)