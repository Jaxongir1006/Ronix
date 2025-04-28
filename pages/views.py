from rest_framework.viewsets import ViewSet
from .serializers import FAQSerializer,AboutUsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ,AboutUs
from django.core.cache import cache

class FaqViewset(ViewSet):
    def list(self, request):
        cache_key = 'faqs_list'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        faqs = FAQSerializer(FAQ.objects.all(), many=True)

        cache.set(cache_key, faqs.data, timeout=60*60) # Cache for 1 hour

        return Response(faqs.data, status=status.HTTP_200_OK)
    
class AboutUsViewset(ViewSet):
    def list(self, request):
        cache_key = 'about_us_list'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        about_us = AboutUsSerializer(AboutUs.objects.all(), many=True)

        cache.set(cache_key, about_us.data, timeout=60*60) # Cache for 1 hour

        return Response(about_us.data, status=status.HTTP_200_OK)