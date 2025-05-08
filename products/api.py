from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet,SubCategoryViewSet
from django.urls import path,include

router = DefaultRouter()

router.register(r'product', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')

urlpatterns = [
    path('', include(router.urls))
]
