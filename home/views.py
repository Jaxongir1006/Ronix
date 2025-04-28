from rest_framework.viewsets import ModelViewSet
from .models import HomeBanner,CustomerReview
from .serializers import HomeBannerSerializer,customerReviewSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

class HomePageContentViewSet(ModelViewSet):
    queryset = HomeBanner.objects.all()
    serializer_class = HomeBannerSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'home_banners_list'
        data = cache.get(cache_key)

        if data:
            return Response(data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, serializer.data, timeout=60*60)

class CustomerReviewViewSet(ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = customerReviewSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'customer_reviews_list'
        data = cache.get(cache_key)

        if data:
            return Response(data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, serializer.data, timeout=60*60)

        return Response(serializer.data, status=status.HTTP_200_OK)