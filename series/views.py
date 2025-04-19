from .serializers import SeriesSerializer, SeriesCategorySerializer, SeriesCategoryDetailSerializer
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import Series, SeriesCategory
from rest_framework.response import Response
from rest_framework import status

class SeriesViewset(ViewSet):
    def list(self, request):
        queryset = Series.objects.all()
        serializer = SeriesSerializer(queryset, many=True)
        return Response(serializer.data)
    
class SeriesCategoryViewset(ViewSet):
    def list(self, request):
        queryset = SeriesCategory.objects.filter(series=request.query_params.get('series_id'))
        if not queryset.exists():
            return Response({"message": "No series categories found for this series."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SeriesCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            queryset = SeriesCategory.objects.get(pk=pk)
            serializer = SeriesCategoryDetailSerializer(queryset)
            return Response(serializer.data)
        except SeriesCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
