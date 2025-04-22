from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewset(ViewSet):
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Order.objects.filter(user_id=request.user.id)
        if not queryset.exists():
            return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderItemViewset(ViewSet):
    def list(self, request):
        queryset = OrderItem.objects.all()
        if not queryset.exists():
            return Response({"message": "No order items found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)