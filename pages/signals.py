from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import FAQ, AboutUs

@receiver([post_save, post_delete], sender=FAQ)
def clear_faq_cache(sender, instance, **kwargs):
    cache_key = 'faqs_list'
    cache.delete(cache_key)

@receiver([post_save, post_delete], sender=AboutUs)
def clear_about_us_cache(sender, instance, **kwargs):
    cache_key = 'about_us_list'
    cache.delete(cache_key)