from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.exceptions import PermissionDenied
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework import status

class CartViewSet(ViewSet):

    def list(self, request):
        user = request.user
        session_id = request.query_params.get('session_id')

        if user.is_authenticated:
            cart, _ = Cart.custom.get_or_create(user=user)
        elif session_id:
            cart, _ = Cart.custom.get_or_create(session_id=session_id)
        else:
            return Response({"error": "User or session_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    http_method_names = ['get','post','put','patch','delete']

    def get_queryset(self):
        user = self.request.user
        session_id = self.request.query_params.get('session_id')

        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user)
        elif session_id:
            return CartItem.objects.filter(cart__session_id=session_id)
        return CartItem.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        session_id = self.request.data.get('session_id')

        if user.is_authenticated:
            cart, _ = Cart.custom.get_or_create(user=user)
        elif session_id:
            cart, _ = Cart.custom.get_or_create(session_id=session_id)
        else:
            raise PermissionDenied("User yoki session_id kerak")

        self._check_cart_owner(cart)
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        cart_item = self.get_object()  # get_object() orqali cart item ni olish
        quantity = self.request.data.get('quantity')

        if quantity is not None:
            cart_item.quantity = quantity  # faqat quantityni yangilaymiz
            cart_item.save()

        self._check_cart_owner(cart_item.cart)  # Cartga egasi bo'lishini tekshiramiz
        serializer.save() 

    def perform_destroy(self, instance):
        self._check_cart_owner(instance.cart)
        instance.delete()

    def _check_cart_owner(self, cart):
        if cart is None:
            return PermissionDenied("Cart mavjud emas")
        user = self.request.user
        session_id = self.request.data.get('session_id') or self.request.query_params.get('session_id')

        if user.is_authenticated and cart.user == user:
            return
        elif not user.is_authenticated and session_id and cart.session_id == session_id:
            return
        raise PermissionDenied("Bu cart sizga tegishli emas.")
