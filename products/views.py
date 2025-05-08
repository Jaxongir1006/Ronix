from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer,ProductForCartSerializer,CategoryDetailsSerializer
from .models import Product,Category,SubCategory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .pagination import CustomPagination

class CategoryViewSet(ViewSet):
    def list(self, request):
        cache_key = 'categories_list'
        data = cache.get(cache_key)

        if data:
            return Response(data, status=status.HTTP_200_OK)

        queryset = Category.objects.language('en').all()
        serializer = CategorySerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 60)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='(?P<category_name>[^/.]+)')
    def category_details(self, request, category_name=None):
        category = get_object_or_404(Category, translations__name=category_name)

        serializer = CategoryDetailsSerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.language('en').all()
    serializer_class = SubCategorySerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        cache_key = 'subcategories_list'
        data = cache.get(cache_key)

        if data:
            return Response(data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, serializer.data, timeout=60*60)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='children')
    def get_children(self, request, pk=None):
        cache_key = f'subcategories_children_{pk}'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        parent = get_object_or_404(SubCategory, pk=pk)
        children = SubCategory.objects.filter(parent=parent)
        serializer = self.get_serializer(children, many=True)
        
        cache.set(cache_key, serializer.data, timeout=60*60)

        return Response(serializer.data)
    
class ProductViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def all(self, request):
        cache_key = 'products_list'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        products = Product.objects.language('en').all()

        paginator = CustomPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductForCartSerializer(paginated_products, many=True)
        response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, serializer.data, timeout=60*60)

        return response

    @action(detail=False, methods=['get'], url_path='(?P<subcategory_name>[^/.]+)')
    def by_subcategory(self, request, subcategory_name=None):
        cache_key = f'products_by_subcategory_{subcategory_name}'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        subcategory = get_object_or_404(SubCategory.objects.language('en'), translation__name=subcategory_name)
        products = Product.objects.language('en').filter(subcategory=subcategory)

        paginator = CustomPagination()
        paginated_products = paginator.paginate_queryset(products, request  )
        
        serializer = ProductForCartSerializer(paginated_products, many=True)
        response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, serializer.data, timeout=60*60)

        return response

    @action(detail=False, methods=['get'], url_path='details/(?P<product_name>[^/.]+)')
    def product_details(self, request, product_name=None):
        product = get_object_or_404(Product.objects.language('en'), translations__name=product_name)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
