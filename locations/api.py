from rest_framework.routers import DefaultRouter
from .views import BranchViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'locations', BranchViewSet, basename='country')
urlpatterns = [
    path('', include(router.urls))
]