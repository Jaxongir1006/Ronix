from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterViewSet, LoginViewSet,ChangePasswordViewSet,UserProfileViewSet,AddressViewSet,GoogleAuthViewSet

router = DefaultRouter()

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'google-auth', GoogleAuthViewSet, basename='google-auth')

urlpatterns = [
    path('', include(router.urls)),
]