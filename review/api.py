from rest_framework.routers import DefaultRouter
from .views import ReviewViewset, RateViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'review', ReviewViewset, basename='review')
router.register(r'rate', RateViewset, basename='rate')

urlpatterns = [
    path('', include(router.urls)),
]