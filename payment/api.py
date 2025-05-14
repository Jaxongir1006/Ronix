from rest_framework.routers import DefaultRouter
from .views import PaymeViewSet

router = DefaultRouter()

router.register(r'payme', PaymeViewSet, basename='payment')