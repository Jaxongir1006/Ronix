from rest_framework.routers import DefaultRouter
from .views import HomePageContentViewSet
from django.urls import path,include

router = DefaultRouter()

router.register(r'home', HomePageContentViewSet, basename='home')

urlpatterns = [
    path('', include(router.urls))
]