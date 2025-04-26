from rest_framework.routers import DefaultRouter
from .views import RegisterLoginView,VerifyCodeView
from django.urls import path, include

router = DefaultRouter()
router.register(r'register', RegisterLoginView, basename='register')
router.register(r'verify-code', VerifyCodeView, basename='verify-code')

urlpatterns =[
    path('', include(router.urls)),
]