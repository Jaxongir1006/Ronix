from rest_framework.routers import DefaultRouter
from .views import HomePageContentViewSet,CustomerReviewViewSet
from django.urls import path,include

router = DefaultRouter()

router.register(r'home', HomePageContentViewSet, basename='home')
router.register(r'customer-review', CustomerReviewViewSet, basename='customer-review')

urlpatterns = [
    path('', include(router.urls))
]