from rest_framework.viewsets import ViewSet
from .serializers import FAQSerializer,NewsletterSubscriberSerializer,AboutUsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ,AboutUs

class FaqViewset(ViewSet):
    def list(self, request):
        faqs = FAQSerializer(FAQ.objects.all(), many=True)
        return Response(faqs.data, status=status.HTTP_200_OK)
    
class NewsletterSubscriberViewset(ViewSet):
    def create(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AboutUsViewset(ViewSet):
    def list(self, request):
        about_us = AboutUsSerializer(AboutUs.objects.all(), many=True)
        return Response(about_us.data, status=status.HTTP_200_OK)