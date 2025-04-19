from rest_framework.routers import DefaultRouter
from .views import DistributorViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'distributors', DistributorViewSet, basename='distributor')

urlpatterns = [
    path('', include(router.urls)),
]