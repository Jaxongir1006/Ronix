from rest_framework.routers import DefaultRouter
from .views import CardViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'card', CardViewSet, basename='card')

urlpatterns = [
    path('', include(router.urls)),
]