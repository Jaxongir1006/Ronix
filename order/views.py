from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer,OrderVerifySerializer,OrderListSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(ViewSet):
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []  # boshqa action'lar uchun permission yo'q
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()

            # Agar serializer dict qaytargan bo'lsa, bu verification uchun
            if isinstance(result, dict) and result.get('status') == False:
                return Response(result, status=status.HTTP_202_ACCEPTED)

            # Agar Order yaratilgan bo'lsa
            return Response({
                "message": "Order created successfully.",
                "order_id": result.id,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        orders = Order.objects.filter(user=user)
        if not orders.exists():
            return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderVerifyView(ViewSet):
    def create(self, request):
        serializer = OrderVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        return Response({"message": "User verified successfully.","tokens": tokens}, status=status.HTTP_200_OK)
    
