from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from .models import HomeBanner,CustomerReview
from .serializers import HomeBannerSerializer,CustomerReviewSerializer
from rest_framework import status
from rest_framework.decorators import action
class HomePageContentViewSet(ViewSet):
    
    @action(detail=False, methods=['get'])
    def banners(self, request):
        banners = HomeBanner.objects.all()
        
        banner_data = HomeBannerSerializer(banners, many=True).data

        return Response({"banners": banner_data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def reviews(self, request):
        reviews = CustomerReview.objects.all()
        
        review_data = CustomerReviewSerializer(reviews, many=True).data

        return Response({"reviews": review_data}, status=status.HTTP_200_OK)