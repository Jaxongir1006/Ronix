from rest_framework.viewsets import ViewSet
from .serializers import FAQSerializer,AboutUsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ,AboutUs

class FaqViewset(ViewSet):
    def list(self, request):
        faqs = FAQSerializer(FAQ.objects.all(), many=True)
        return Response(faqs.data, status=status.HTTP_200_OK)
    
class AboutUsViewset(ViewSet):
    def list(self, request):
        about_us = AboutUsSerializer(AboutUs.objects.all(), many=True)
        return Response(about_us.data, status=status.HTTP_200_OK)