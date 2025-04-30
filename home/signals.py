from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import CustomerReview, HomeBanner

@receiver([post_save, post_delete], sender=CustomerReview)
def clear_customer_review_cache(sender, instance, **kwargs):
    cache_key = 'customer_reviews_list'
    cache.delete(cache_key)

@receiver([post_save, post_delete], sender=HomeBanner)
def clear_home_banner_cache(sender, instance, **kwargs):
    cache_key = 'home_banners_list'
    cache.delete(cache_key)