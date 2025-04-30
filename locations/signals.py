from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Branch

@receiver([post_save, post_delete], sender=Branch)
def clear_cache_after_save(sender, instance, **kwargs):
    cache_key = 'branches_list'
    cache.delete(cache_key)

