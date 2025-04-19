from rest_framework import serializers
from .models import Distributor

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        exclude = ['created_at', 'is_active']