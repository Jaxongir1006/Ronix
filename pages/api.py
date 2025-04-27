from rest_framework.routers import DefaultRouter
from .views import FaqViewset, AboutUsViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'faq', FaqViewset, basename='faq')
router.register(r'about-us', AboutUsViewset, basename='about-us')

urlpatterns = [
    path('', include(router.urls)),
]