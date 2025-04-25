from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order

class OrderViewSet(ViewSet):
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Order created successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        queryset = Order.objects.language('en').filter(user=request.user)
        if not queryset.exists():
            return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)