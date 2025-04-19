from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from .models import HomeBanner, CustomerReview
from .serializers import HomeBannerSerializer, CustomerReviewSerializer,ProductSerializer
from products.serializers import CategorySerializer
from products.models import Category,Product

class HomePageContentViewSet(ViewSet):
    def list(self, request):
        banners = HomeBanner.objects.all()
        reviews = CustomerReview.objects.all()
        category = Category.objects.all()[10]
        product = Product.objects.all()

        banner_data = HomeBannerSerializer(banners, many=True).data
        review_data = CustomerReviewSerializer(reviews, many=True).data
        category_data = CategorySerializer(category, many=True).data
        product_data = ProductSerializer(product, many=True).data

        return Response({
            'banners': banner_data,
            'customer_reviews': review_data,
            'category_data':category_data,
            'product_data':product_data,
        })

