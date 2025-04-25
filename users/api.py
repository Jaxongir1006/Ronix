from rest_framework.routers import DefaultRouter
from .views import UserViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'user', UserViewset, basename='user')


urlpatterns =[
    path('', include(router.urls)),
]