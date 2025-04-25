from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import HomeBanner
from .serializers import HomeBannerSerializer
from rest_framework import status
class HomePageContentViewSet(ViewSet):

    def list(self, request):
        banners = HomeBanner.objects.all()
        
        banner_data = HomeBannerSerializer(banners, many=True).data

        return Response({"banners": banner_data}, status=status.HTTP_200_OK)
