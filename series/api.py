from .views import SeriesViewset,SeriesCategoryViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'series', SeriesViewset, basename='series')
router.register(r'series-category', SeriesCategoryViewset, basename='series-category')

urlpatterns = [
    path('', include(router.urls)),
]