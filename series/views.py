from .serializers import SeriesSerializer, SeriesCategorySerializer, SeriesCategoryDetailSerializer
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import Series, SeriesCategory
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

class SeriesViewset(ViewSet):
    def list(self, request):
        cache_key = "series_list"
        data = cache.get(cache_key)

        if data is None:
            queryset = Series.objects.all()
            serializer = SeriesSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)
        return Response(data)


class SeriesCategoryViewset(ViewSet):
    def list(self, request):
        series_id = request.query_params.get('series_id')
        cache_key = f"series_categories_{series_id}"
        data = cache.get(cache_key)

        if data is None:
            queryset = SeriesCategory.objects.filter(series=series_id)
            if not queryset.exists():
                return Response({"message": "No series categories found for this series."}, status=status.HTTP_404_NOT_FOUND)
            serializer = SeriesCategorySerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f"series_category_detail_{pk}"
        data = cache.get(cache_key)

        if data is None:
            try:
                instance = SeriesCategory.objects.get(pk=pk)
                serializer = SeriesCategoryDetailSerializer(instance)
                data = serializer.data
                cache.set(cache_key, data, timeout=60 * 5)
            except SeriesCategory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data)
