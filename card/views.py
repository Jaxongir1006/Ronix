from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CardSerializer
from .models import Card
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated

class CardViewSet(ViewSet):
    """
    A viewset for managing credit card information.
    """
    permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "This card number is already registered."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):

        cards = Card.objects.filter(user=request.user)
        if not cards.exists():
            return Response({"message": "No cards found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CardSerializer(cards, many=True)
        card_data = serializer.data

        return Response(card_data, status=status.HTTP_200_OK)