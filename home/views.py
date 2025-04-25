from rest_framework.viewsets import ModelViewSet
from .models import HomeBanner,CustomerReview
from .serializers import HomeBannerSerializer,customerReviewSerializer
class HomePageContentViewSet(ModelViewSet):
    queryset = HomeBanner.objects.all()
    serializer_class = HomeBannerSerializer
    http_method_names = ['get']


class CustomerReviewViewSet(ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = customerReviewSerializer
    http_method_names = ['get']

