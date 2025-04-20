from .views import ContactUsViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'contact', ContactUsViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls))
]