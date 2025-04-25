from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import ProductSerializer,CategorySerializer,SpecificationSerializer,ProductDetailSerializer,ProductImagesSerializer,SubCategorySerializer
from .models import Product,Category,SubCategory,ProductDetail,ProductImages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.language('en').all()
    serializer_class = CategorySerializer
    http_method_names = ['get']


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.language('en').all()
    serializer_class = SubCategorySerializer
    http_method_names = ['get']

    @action(detail=False, methods=['get'], url_path='(?P<category_name>[^/.]+)')
    def by_category(self, request, category_name=None):
        category = get_object_or_404(Category, translations__name=category_name)
        subcategories = SubCategory.objects.filter(category=category, parent__isnull=True)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='children')
    def get_children(self, request, pk=None):
        parent = get_object_or_404(SubCategory, pk=pk)
        children = SubCategory.objects.filter(parent=parent)
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)
    
class ProductViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def all(self, request):
        products = Product.objects.language('en').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='(?P<subcategory_name>[^/.]+)')
    def by_subcategory(self, request, subcategory_name=None):
        subcategory = get_object_or_404(SubCategory.objects.language('en'), translation__name=subcategory_name)
        products = Product.objects.language('en').filter(subcategory=subcategory)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def specifications(self, request, pk=None):
        product = get_object_or_404(Product.objects.language('en'), pk=pk)

        if not hasattr(product, 'specifications') or product.specifications is None:
            return Response({"detail": "Specification not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecificationSerializer(product.specifications)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        product = get_object_or_404(Product.objects.language('en'), pk=pk)
        if not hasattr(product, 'details') or product.details is None:
            return Response({"detail": "Product details not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product.details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        product = get_object_or_404(Product.objects.language('en'), pk=pk)
        if not hasattr(product, 'images') or product.images is None:
            return Response({"detail": "Product images not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductImagesSerializer(product.images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)