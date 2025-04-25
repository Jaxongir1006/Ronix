from rest_framework.routers import DefaultRouter
from .views import SendSMSView,SendVerificationEmailView
from django.urls import path, include

router = DefaultRouter()
router.register(r'send-sms', SendSMSView, basename='send-sms')
router.register(r'send-email', SendVerificationEmailView, basename='send-email')


urlpatterns = [
    path('', include(router.urls)),
]