from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,VerificationViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-verify', VerificationViewSet, basename='order-verify')
# router.register(r'order-verify', OrderVerifyView, basename='order-verify')


urlpatterns = [
    path('', include(router.urls)),
]