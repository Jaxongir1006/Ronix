from .views import BlogViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'blog', BlogViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]