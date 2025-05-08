from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet,CartViewSet
from django.urls import path,include

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls))
]