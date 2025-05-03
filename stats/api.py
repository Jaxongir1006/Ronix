from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserStatsAPIView

router = DefaultRouter()

router.register(r'admin-stats', UserStatsAPIView, basename='admin-stats')

urlpatterns = [
    path('', include(router.urls)),
]