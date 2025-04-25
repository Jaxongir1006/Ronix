from rest_framework import serializers

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()