from rest_framework import viewsets
from .models import Content
from .serializers import ContentSerializer
from django.core.cache import cache
from rest_framework.response import Response

class ContentViewSet(viewsets.ViewSet):
    def list(self, request):
        cache_key = "content_list"
        data = cache.get(cache_key)

        if not data:
            queryset = Content.objects.all()
            serializer = ContentSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f"content_detail_{pk}"
        data = cache.get(cache_key)

        if not data:
            try:
                content = Content.objects.get(pk=pk)
            except Content.DoesNotExist:
                return Response({"detail": "Not found."}, status=404)

            serializer = ContentSerializer(content)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)
        return Response(data)
