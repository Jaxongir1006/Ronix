from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,OrderVerifyView
from django.urls import path, include

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-verify', OrderVerifyView, basename='order-verify')

urlpatterns = [
    path('', include(router.urls)),
]