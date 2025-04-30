from rest_framework import serializers
from .models import Card
from datetime import date

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_number', 'cardholder_name', 'expiration_date', 'cvv']
    
    def validate_expiration_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value