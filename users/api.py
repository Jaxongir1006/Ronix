from rest_framework.routers import DefaultRouter
from .views import RegisterView,VerifyCodeView,GoogleAuthViewSet,UserProfileViewSet,LoginViewSet,ResetPasswordViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'register', RegisterView, basename='register')
router.register(r'verify-code', VerifyCodeView, basename='verify-code')
router.register(r'google-auth/callback', GoogleAuthViewSet, basename='google-auth')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'reset-password', ResetPasswordViewSet, basename='reset-password')

urlpatterns =[
    path('', include(router.urls)),
]