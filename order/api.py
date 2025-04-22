from rest_framework.routers import DefaultRouter
from .views import OrderViewset,OrderItemViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'order', OrderViewset, basename='order')
router.register(r'order-item', OrderItemViewset, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
]