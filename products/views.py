from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import ProductSerializer,CategorySerializer,ProductByCategorySerializer
from .models import Product,Category


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get']
    queryset = Product.objects.all()

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    http_method_names = ['get']
    queryset = Category.objects.all()


class ProductByCategory(ModelViewSet):
    serializer_class = ProductByCategorySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Product.objects.filter(category = self.request.category)