from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer,OrderReadSerializer
from .models import Order,OrderItem
from rest_framework.decorators import action
from cart.models import Cart
from django.db import transaction
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()

    @action(detail=False, methods=['post'], url_path='create-from-cart')
    def create_from_cart(self, request):
        user = request.user
        session_id = request.data.get('session_id') or request.COOKIES.get('sessionid')

        cart = None
        if user.is_authenticated:
            cart = Cart.custom.prefetch_related('cart_items__product').filter(user=user).first()
        elif session_id:
            cart = Cart.custom.prefetch_related('cart_items__product').filter(session_id=session_id).first()

        if not cart:
            return Response({'detail': 'Cart not found.'}, status=404)

        if not cart.cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=400)

        with transaction.atomic():
            total_price = sum(
                item.product.price * item.quantity for item in cart.cart_items.all()
            )

            order = Order.objects.create(
                user=cart.user if cart.user else None,
                total_price=total_price,
            )

            for item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart.cart_items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderReadSerializer

class VerificationViewSet(ViewSet):
    
    def create(self, request):
        code = request.data.get('code')
        user = User.objects.filter(verification_code=code).first()

        if user:
            user.is_verified = True
            user.save()
            
            refresh = RefreshToken.for_user(user)
            token = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

