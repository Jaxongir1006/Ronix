from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer,OrderReadSerializer
from .models import Order,OrderItem
from rest_framework.permissions import IsAuthenticated
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

    @action(detail=False, methods=['post'])
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

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'detail': 'Only pending orders can be verified'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'verified'
        order.save()
        return Response({'detail': 'Order verified'}, status=status.HTTP_200_OK)

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


# class OrderViewSet(ViewSet):
    
#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = []  # boshqa action'lar uchun permission yo'q
#         return [permission() for permission in permission_classes]

#     def create(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             result = serializer.save()

#             # Agar serializer dict qaytargan bo'lsa, bu verification uchun
#             if isinstance(result, dict) and result.get('status') == False:
#                 return Response(result, status=status.HTTP_202_ACCEPTED)

#             # Agar Order yaratilgan bo'lsa
#             return Response({
#                 "message": "Order created successfully.",
#                 "order_id": result.id,
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request):
#         user = request.user
#         if not user.is_authenticated:
#             return Response({"message": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

#         orders = Order.objects.filter(user=user)
#         if not orders.exists():
#             return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = OrderListSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class OrderVerifyView(ViewSet):
#     def create(self, request):
#         serializer = OrderVerifySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         tokens = serializer.save()
#         return Response({"message": "User verified successfully.","tokens": tokens}, status=status.HTTP_200_OK)
    