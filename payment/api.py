from rest_framework.routers import DefaultRouter
from .views import PaymeCallbackAPIView,ClickPaymentViewSet,ClickTransactionViewSet
from .payment_merchant import PaymeViewSet
from django.urls import path,include

router = DefaultRouter()

router.register(r'payme', PaymeViewSet, basename='payme')
router.register(r'payme/callback', PaymeCallbackAPIView, basename='payme-callback')
router.register(r'click', ClickPaymentViewSet, basename='click')
router.register(r'click/transaction', ClickTransactionViewSet, basename='click-transaction')

urlpatterns = [
    path('', include(router.urls))
]       