from rest_framework.routers import DefaultRouter
from .views import RegisterLoginView,VerifyCodeView,GoogleAuthViewSet,UserProfileViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'register', RegisterLoginView, basename='register')
router.register(r'verify-code', VerifyCodeView, basename='verify-code')
router.register(r'google-auth/callback', GoogleAuthViewSet, basename='google-auth')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns =[
    path('', include(router.urls)),
]