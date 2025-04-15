from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet,ProductByCategory
from django.urls import path,include

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'product', ProductByCategory, basename='product')

urlpatterns = [
    path('', include(router.urls))
]
