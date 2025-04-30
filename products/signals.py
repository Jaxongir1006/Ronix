from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category,SubCategory,Product

@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, **kwargs):
    
    cache_key = 'categories_list'

    cache.delete(cache_key)

@receiver([post_save, post_delete], sender=SubCategory)
def clear_subcategory_cache(sender, **kwargs):
    
    cache_key = 'subcategories_list'

    cache.delete(cache_key)

@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, **kwargs):
    
    cache_key = 'products_list'

    cache.delete(cache_key)
